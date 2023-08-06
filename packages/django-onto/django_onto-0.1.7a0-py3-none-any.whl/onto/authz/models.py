import logging
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType
from django.db import models

from onto.models import Entity, EntityModel, XAttrsMixin

from . import utils

audit_log = logging.getLogger("authz")

def user_ct_id():
    return ContentType.objects.get_for_model(get_user_model()).pk


# TODO add preferred language / timezone
class AbstractUser(EntityModel, AbstractUser):
    """
    Swaps `first_name`, `last_name` fields for more generic `display_name`.
    """
    class Meta:
        abstract = True

    class ArchiveManager(EntityModel.ArchiveManager, UserManager):
        pass

    class Manager(ArchiveManager):
        def get_queryset(self):
            return super().get_queryset().exclude(archived=True)


    objects = Manager()
    objects_archive = ArchiveManager()

    display_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    @property
    def first_name(self):
        if not self.display_name:
            return ""

        return self.display_name.split()[0]
        
    @property
    def last_name(self):
        if not self.display_name:
            return ""

        tokens = self.display_name.split()
        if len(tokens) <= 1:
            return ""

        return tokens[-1]

    # Technically, this is already monkeypatched onto EntityModel, but we also specify it here for a little more API clarity.
    def is_authorized(self, action, resource):
        """
        Returns True if the User is authorized to perform the `action` on the `resource`, otherwise False.
        """
        return is_authorized(self, action, resource)

    def __str__(self):
        return self.display_name or self.username or self.email


class Domain(models.Model):
    """
    A unique dot-delimited string representing a set of Entities.
    """
    class Manager(models.Manager):
        def get_by_natural_key(self, name):
            return self.get(name=name)

    objects = Manager()

    name = models.SlugField(
        unique=True,
        max_length=255,
        help_text="Fully-qualified Domain Name. Must be unique.",
    )

    entities = models.ManyToManyField(
        "onto.Entity",
        related_name="domains",
        blank=True,
        through="onto_authz.Membership",
        help_text="Entities contained in this domain."
    )

    active = models.BooleanField(
        default=True,
        help_text="When inactive, this domain cannot grant authorization."
    )

    def add(self, obj: EntityModel) -> "Membership":
        """
        Add an object (or entity_id) to the domain, returning the associated Membership object.
        """
        if isinstance(obj, models.Model):
            pk = obj.pk
        else:
            pk = obj

        membership, created = self.memberships.get_or_create(entity_id=pk)
        return membership

    def get(self, obj: EntityModel) -> "Membership":
        """
        Return the Membership associated with an object or entity_id. Raises DoesNotExist if not a member.
        """
        if isinstance(obj, models.Model):
            pk = obj.pk
        else:
            pk = obj

        return self.memberships.get(entity_id=pk)
    
    def remove(self, obj: EntityModel):
        """
        Remove an object (or entity_id) from the domain, if it exists.
        """
        if isinstance(obj, models.Model):
            pk = obj.pk
        else:
            pk = obj

        return self.memberships.filter(entity_id=pk).delete()
    
    def xfilter(self, **filters) -> "Membership.QuerySet":
        return self.memberships.xfilter(**filters)

    @property
    def subdomains(self):
        return Domain.objects.filter(name__startswith=self.name+'.')

    def create_subdomain(self, subdomain_name, **kwargs) -> "Domain":
        """
        Creates a new domain with the current domain's name followed by `.subdomain_name`.

        Example:
        >>> domain1 = Domain.objects.create(name="acme")
        >>> domain2 = domain1.create_subdomain("accounting")
        >>> domain2.name
        "acme.accounting"
        >>> domain2 in domain1.subdomains
        True
        """
        subdomain, created = Domain.objects.get_or_create(name=f"{self.name}.{subdomain_name}", **kwargs)
        return subdomain

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name
    
    def __contains__(self, item: EntityModel):
        return self.memberships.filter(entity_id=item.pk).exists()


class Membership(XAttrsMixin, models.Model):
    """
    Represents the Domain-Entity M2M relationship.

    Has its own set of `xattrs`, allowing arbitrary data to be associated with individual relationships.
    """
    class QuerySet(XAttrsMixin.QuerySet, models.QuerySet):
        @property
        def entities(self):
            return Entity.objects.filter(pk__in=self.values("entity").distinct())

        @property
        def domains(self):
            return Domain.objects.filter(pk__in=self.values("domain").distinct())

        def as_model(self, *models: models.Model, annotate_xattrs=False):
            """
            Returns a dictionary mapping Models to querysets of objects of that type, as contained in the Memberships.

            If exactly one model is specified, returns that queryset directly.

            If `annotate_xattrs` is True, annotate each object with its Membership `xattrs`; this uses a raw query for efficiency and cannot be further chained.
            """
            results = dict()
            models = models or {ct.model_class() for ct in ContentType.objects.filter(pk__in=self.values_list("content_type", flat=True).distinct())}
            for model in models:
                ct = ContentType.objects.get_for_model(model)
                matching = self.filter(entity__content_type=ct)  # Could remove the contenttype filter to remove a join at cost of larger IN, may want to profile
                if not annotate_xattrs:
                    results[model] = model.objects.filter(entity_id__in=matching.values("entity_id"))
                else:
                    results[model] = model.objects.raw(f"SELECT model.*, ms.xattrs::json FROM {model._meta.db_table} model INNER JOIN {Membership._meta.db_table} ms ON model.entity_id=ms.entity_id WHERE ms.id IN ({matching.values('id').query});")

            if len(models) == 1:
                return results[model]

            return results
        

    objects = QuerySet.as_manager()

    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    @property
    def object(self):
        return self.entity.content_object

    def __str__(self):
        return f"{self.entity}@{self.domain}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["entity", "domain"], name="%(app_label)s_%(class)s_unique")
        ]

class Action(models.Model):
    """
    An action that can be authorized. Does not specify what the action does.
    """
    class Manager(models.Manager):
        def get_by_natural_key(self, source_type_nk, label, target_type_nk):
            source_type = ContentType.objects.get_by_natural_key(*source_type_nk.split('.'))
            target_type = ContentType.objects.get_by_natural_key(*target_type_nk.split('.'))
            return self.get(label=label, source_type=source_type, target_type=target_type)

        def get_by_str(self, string):
            """
            Deserializes a __str__ into an Action object using the natural key. 
            """
            tokens = string.split('__')
            if len(tokens) == 2:
                tokens = (settings.AUTH_USER_MODEL.lower(), *tokens)
            return self.get_by_natural_key(*tokens)

    objects = Manager()

    label = models.SlugField(
        max_length=255,
        help_text="Internal reference key for this action.",
    )
    source_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=user_ct_id,
        related_name='actions_as_source',
        help_text="The ContentType of objects that perform this action, defaults to AUTH_USER_MODEL."
    )
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='actions_as_target',
        help_text="The ContentType of objects that this action affects."
    )
    default_permit = models.BooleanField(
        default=True,
        help_text="Whether this action is allowed to be performed by default. If False, a Policy must explicitly grant it."
    )
    dispatch_changes = models.BooleanField(
        default=False,
        help_text="Whether to track the state of all entitlements for this action, and emit signals when they change."
    )

    title = models.CharField(
        max_length=255,
        help_text="A human-readable name for this action."
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Describe the action, including its intended purpose."
    )

    def natural_key(self):
        return (
        '.'.join(self.source_type.natural_key()),
        self.label,
        '.'.join(self.target_type.natural_key()),
        )

    def save(self, *args, **kwargs):
        self.label = re.sub(r'_{2,}','_', self.label)  # collapse underscores
        super().save(*args, **kwargs)
        
    def __str__(self):
        return "__".join(self.natural_key())

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["label", "target_type", "source_type"], name="%(app_label)s_%(class)s_unique")
        ]


class Policy(models.Model):
    """
    A Policy defines sets of valid Principals, Actions, and Resources, respectively.
    A valid Principal is authorized to perform any of the valid Actions on any of the valid Resources.
    """
    class Manager(models.Manager):
        def create_with_actions(self, *actions, **kwargs):
            policy = self.create(**kwargs)
            for action in actions:
                if isinstance(action, str):
                    action = Action.objects.get_by_str(action)
                policy.actions.add(action)

            return policy

    class QuerySet(models.QuerySet):
        pass

    objects = Manager.from_queryset(QuerySet)()

    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
        related_name="policies",
    )
    label = models.SlugField(
        max_length=255,
    )

    principal_filters = models.JSONField(
        default=dict,
        help_text="This policy affects entities (as source principals) that match this specification (or all entities in the domain if NULL).",
    )
    actions = models.ManyToManyField(
        Action,
        related_name="policies",
    )
    resource_filters = models.JSONField(
        default=dict,
        help_text="This policy affects entities (as target resources) that match this specification (or all entities in the domain if NULL).",
    )
    disabled = models.BooleanField(
        default=False,
        help_text="When this policy is disabled, it will not be considered for authorization."
    )

    @property
    def principals(self) -> Entity.QuerySet:
        """
        All principal Entities that this Policy currently applies to.
        """
        return self.domain.entities.filter(content_type__in=self.actions.values("source_type").distinct(), **self.principal_filters)

    @property
    def resources(self) -> Entity.QuerySet:
        """
        All target Entities (i.e. resources) that this Policy currently applies to.
        """
        return self.domain.entities.filter(content_type__in=self.actions.values("target_type").distinct(), **self.resource_filters)

    def __str__(self):
        return f"{self.domain}.{self.label}"


    class Meta:
        verbose_name_plural = "policies"
        constraints = [
            models.UniqueConstraint(fields=["label", "domain"], name="%(app_label)s_%(class)s_unique")
        ]


class Entitlement(models.Model):
    """
    Entitlements track the state of a particular authorized action. They are managed automatically and should not be modified manually.
    See "./signals.py" for more details on the automated Entitlement system.
    """
    principal = models.ForeignKey(
        "onto.Entity",
        on_delete=models.CASCADE,
        editable=False,
        related_name="entitlements_as_principal",
    )
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE, 
        editable=False,
        related_name="entitlements",
    )
    resource = models.ForeignKey(
        "onto.Entity",
        on_delete=models.CASCADE,
        editable=False,
        related_name="entitlements_as_resource",
    )
    domain = models.ForeignKey(
        "onto_authz.Domain",
        on_delete=models.CASCADE,
        editable=False,
        related_name="entitlements",
    )
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        null=True,
        editable=False,
        related_name="entitlements",
    )

    @property
    def peers(self):
        return Entitlement.objects.filter(principal=self.principal, resource=self.resource, action=self.action).exclude(id=self.id)

@utils.monkeypatch_method(EntityModel)
def is_authorized(principal: Entity, action: Action, resource: Entity):
    """
    Returns True iff the `principal` Entity (or EntityModel subclass) is allowed to perform `action` on `resource`, based on Domain Membership, Policies, and other factors.
    """

    principal = Entity.objects.from_object(principal)
    resource = Entity.objects.from_object(resource)

    if isinstance(action, str):
        action = Action.objects.get(label=action, source_type=principal.content_type, target_type=resource.content_type)
    elif action.source_type != principal.content_type or action.target_type != resource.content_type:
        raise ValueError(f"the action `{action}` does not match the provided principal's and resources' content_types.")

    intersection = set(principal.domains.filter(active=True) & resource.domains.filter(active=True))
    if not intersection:  # Entities MUST share a domain to interact.
        audit_log.info(f"DENIED {principal} {action.label} {resource} (no shared domain with active=True)")
        return False

    if action.default_permit and not resource.restricted:  # If the action is not access-controlled, and they entities share a domain, access is granted.
        audit_log.info(f"ALLOWED {principal} {action.label} {resource} (shared {intersection})")
        return True

    # For restricted actions, we must search applicable policies
    for policy in Policy.objects.filter(
        disabled=False,
        domain__in=intersection,
        actions=action,
    ):
        if (
            policy.principals.filter(pk=principal.pk).exists() 
            and policy.resources.filter(pk=resource.pk).exists()
        ):
            audit_log.info(f"ALLOWED {principal} {action.label} {resource} (matched policy {policy})")
            return True
    
    audit_log.info(f"DENIED {principal} {action.label} {resource} (no policy match)")
    return False

@utils.monkeypatch_method(EntityModel)
def get_authorized_resources(principal: Entity, action: Action, resource_model: models.base.ModelBase):
    """
    Returns a QuerySet of `resource_model` containing all objects that `principal` is currently authorized to perform `action` on.

    For example, answers the question "which Articles can this User 'edit'?"
    """

    principal = Entity.objects.from_object(principal)

    # NOTE: this does not currently handle EntityModel subclasses that have overriden `entity_pk_field`
    if issubclass(resource_model, EntityModel):
        resource_ct = ContentType.objects.get_for_model(resource_model)
    else:
        resource_ct = ContentType.objects.get_for_model(resource_model._meta.get_field(resource_model.entity_pk_field).remote_field.model)

    if isinstance(action, str):
        action = Action.objects.get(label=action, source_type=principal.content_type, target_type=resource_ct)

    if action.default_permit:
        resource_entities = Entity.objects.filter(restricted=False, domains__in=principal.domains.filter(active=True))
    else:
        resource_entities = Entity.objects.none()

    for policy in Policy.objects.filter(
      disabled=False,
      domain__in=principal.domains.filter(active=True),
      actions=action
      ):
        if not policy.principals.filter(pk=principal.pk).exists():
            continue
        resource_entities = resource_entities.union(policy.resources.values("pk"))

    return resource_entities.as_model(resource_model)

@utils.monkeypatch_method(EntityModel)
def get_authorized_principals(resource: Entity, action: Action, principal_model: models.base.ModelBase):
    """
    Returns a QuerySet of `principal_model` containing all objects that are currently authorized to perform `action` on `resource`.

    For example, answers the question "which Users can 'edit' this Article?"
    """

    resource = Entity.objects.from_object(resource)

    # NOTE: this does not currently handle EntityModel subclasses that have overriden `entity_pk_field`
    if issubclass(principal_model, EntityModel):
        principal_ct = ContentType.objects.get_for_model(principal_model)
    else:
        principal_ct = ContentType.objects.get_for_model(principal_model._meta.get_field(principal_model.entity_pk_field).remote_field.model)

    if isinstance(action, str):
        action = Action.objects.get(label=action, source_type=principal_ct, target_type=resource.content_type)

    if action.default_permit:
        principal_entities = Entity.objects.filter(domains__in=resource.domains.filter(active=True))
    else:
        principal_entities = Entity.objects.none()

    for policy in Policy.objects.filter(
      disabled=False,
      domain__in=resource.domains.filter(active=True),
      actions=action
      ):
        if not policy.resources.filter(pk=resource.pk).exists():
            continue
        principal_entities = principal_entities.union(policy.principals.values("pk"))

    return principal_entities.as_model(principal_model)