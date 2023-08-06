import logging

from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils import timezone

from .mixins import XAttrsMixin
from .utils import get_entity_pk

#from django.contrib.postgres.indexes import GinIndex

logger = logging.getLogger(__name__)


class Entity(XAttrsMixin, models.Model):
    """
    The central model of Onto, the Entity table contains a record for each record of every `EntityModel` subclass.

    Entities should NOT be created directly; they are automatically created whenever a new instance of an `EntityModel` subclass is created.
    """
    class Meta:
        verbose_name_plural = "entities"
#        indexes = [
#            GinIndex(fields=['xattrs']),
#            ]  # TODO Allow users to declare deeper indexes against xattrs

    class ArchiveManager(models.Manager):
        def from_object(self, obj) -> "Entity":
            """
            Return the primary Entity associated with any object, using its `entity_pk_field` attribute.

            EntityModel subclasses have this attribute by default, other classes must define it explicitly or this method will fail.
            """
            if isinstance(obj, Entity):
                return obj

            return self.get(pk=get_entity_pk(obj))

    class Manager(ArchiveManager):
        """
        Excludes archived entities.
        """
        def get_queryset(self):
            return super().get_queryset().exclude(archived_time__isnull=False)


    class QuerySet(models.QuerySet):
        def archive(self):
            for entity in self:
                entity.archive()

        def restore(self):
            for entity in self:
                entity.restore()

        def xfilter(self, **filters):
            """
            Include only entities with the specified extended attribute (`xattrs`).
            """
            return self.filter(**{f"xattrs__{query}":value for query,value in filters.items()})

        def as_model(self, *models: models.Model):
            """
            Returns a dictionary mapping Models to querysets of objects of that type.

            If exactly one model is specified, returns that queryset directly.

            Examples:

            >>> Entity.objects.filter(...).as_model(User)
            <QuerySet [<User: alice>, <User: bob>, ...]>

            >>> Entity.objects.filter(...).as_model(User, Region, ...)
            {
                User: <QuerySet [<User: alice>, <User: bob>, ...]>,
                Region: <QuerySet [<Region: fredonia>, ...]>,
                ...
            }
            """
            results = dict()
            models = models or {ct.model_class() for ct in ContentType.objects.filter(pk__in=self.values_list("content_type", flat=True).distinct())}
            pks = self.values("pk")
            for model in models:
                results[model] = model.objects.filter(**{f"{model.entity_pk_field}__in":pks})

            if len(models) == 1:
                return results[model]

            return results


    objects: Manager = Manager.from_queryset(QuerySet)()
    objects_archive: ArchiveManager = ArchiveManager.from_queryset(QuerySet)()

    entity_pk_field = "id"
    id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT, editable=False)
    content_object = GenericForeignKey('content_type', 'id')

    created_time = models.DateTimeField(
        auto_now_add=True,
        help_text="When this entity and associated object were created."
    )
    archived_time = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        help_text="When this entity and its associated object were last archived."
    )

    if apps.is_installed("onto.authz"):
        restricted = models.BooleanField(
            "Access restricted",
            default=False,
            blank=True,
            help_text="When False, access to this object may be granted simply by sharing a Domain. When True, there must also be a matching Policy.",
        )

    @property
    def url(self):
        """
        Return a relative link to the details page for this object.
        """
        # TODO add prefix from settings?
        return '/'.join(("", *self.content_type.natural_key(), str(self.id)))

    def archive(self):
        self.content_object.archived = True
        self.content_object.save(update_fields=["archived"])
        self.archived_time = timezone.now()
        return self.save(update_fields=["archived_time"])

    def related_objects(self, model) -> models.QuerySet:
        """
        Return a QuerySet of `model` where `model.entity_pk_field` resolves to this Entity.
        """
        return model.objects.filter(**{f"{model.entity_pk_field}":self.pk})

    def __str__(self):
        return '.'.join((*self.content_type.natural_key(), str(self.content_object)))

class EntityModel(models.Model):
    """
    Abstract class that overrides the default `id` primary key with a OneToOne field to the Entity table called `entity_id`.
    Also adds a `archived` BooleanField to allow "soft-deletion".

    This means each EntityModel represents two database records, one for the usual table, and one in the Entity table.
    This gives us the powerful ability to query all Entities at once with zero joins, even if the underlying schemas are incompatible.

    However, it does mean we must be careful with which models inherit this, so as to not pollute this precious global "namespace".
    Good candidates: Person, Location, Organization, Asset, System, Country, ~Article, etc. 
    (Entities or "business objects" that *exist* outside this database or would benefit strongly from the querying functionality.)
    Bad candidates: Event, Log, sensor reading, relationship/m2m tables, transaction record, etc.

    Otherwise, this EntityModel behaves like any other base Model subclass.
    """
    class Meta:
        abstract = True

    class QuerySet(models.QuerySet):
        @property
        def entities(self):
            """
            Return the QuerySet of corresponding Entities. This is a nested query, so could be slow for large QuerySets!
            """
            return Entity.objects_archive.filter(pk__in=self)

        def xfilter(self, **filters):
            """
            Include only entities with the specified extended attribute (`xattrs`).
            """
            return self.filter(**{f"entity__xattrs__{query}":value for query,value in filters.items()})

        def delete(self, *args, **kwargs):
            """
            Delete all objects in the QuerySet by deleting their associated Entities.
            """
            return self.entities.delete(*args, **kwargs)

        def archive(self):
            """
            "Soft-deletes" objects in the QuerySet, preventing them from showing up in the default `objects` Manager.

            Use the `objects_archive` Manager to query both archived and unarchived objects.
            """
            with transaction.atomic():
                self.entities.update(archived_time=timezone.now())
                self.update(archived=True)

        def restore(self):
            """
            Reverses the archiving i.e. "soft-deletion" of objects in the QuerySet (see `.archive()`).
            
            Note that the default `objects` Manager won't select archived objects, so this method will only be useful on the `objects_archive` Manager.
            """
            with transaction.atomic():
                self.update(archived=False)
                self.entities.update(archived_time=None)


    class ArchiveManager(models.Manager.from_queryset(QuerySet)):
        use_in_migrations = False  # Not worth the hassle/footguns

    class Manager(ArchiveManager):
        def get_queryset(self):
            return super().get_queryset().exclude(archived=True)

    objects = Manager()
    objects_archive = ArchiveManager()

    entity_pk_field = "entity_id"
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="+",
        editable=False,
    )
    archived = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,
        help_text="True indicates the object has been archived and won't appear in most queries."
    )

    @property
    def content_type(self):
        # This is cached by default.
        return ContentType.objects.get_for_model(type(self))

    def xget(self, key, default=None):
        """
        Get the associated entity's `xattrs` value by `key`, or `default` if it doesn't exist.
        """
        return self.entity.xget(key, default=default)

    def xset(self, **data) -> Entity:
        """
        Update the associated entity's `xattrs` with the provided keyword arguments.

        Don't forget to `xsave()`!
        """
        return self.entity.xset(**data)

    def xdel(self, *keys) -> Entity:
        """
        Delete the `keys` from the `xattrs` of the associated entity.

        Don't forget to `xsave()`!
        """
        return self.entity.xdel(*keys)

    def xsadd(self, **data) -> Entity:
        """
        Add to set. Attempt to add each of the keyword values to the sets at their respective keys in the associated entity's `xattrs`.

        Don't forget to `xsave()`!

        If a key does not exist, create a set there.

        If a key exists but is not a list, raise a ValueError.

        If the values are iterable (non-string), they *will* be unpacked/flattened!
        Example:
        >>> user.xsadd(roles="viewer")
        >>> user.xsadd(roles={"editor", "admin"})
        >>> user.xget("roles")
        ["viewer", "editor", "admin"]  # note how it is a flat list
        """
        return self.entity.xsadd(**data)

    def xsremove(self, **data) -> Entity:
        """
        Remove from set. Attempt to remove each of the keyword values from the sets at their respective keys in the associated entity's `xattrs`.

        Don't forget to `xsave()`!

        If a key exists but is not a list, raise a ValueError.

        If the values are iterable (non-string), they *will* be unpacked/flattened!
        """
        return self.entity.xsremove(**data)

    def xsave(self, *args, **kwargs):
        """
        `save` the `xattrs` field, committing it to the database.
        """
        return self.entity.xsave(*args, **kwargs)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            created = self._state.adding
            if created:
                if not hasattr(self, "entity"):
                    ct = ContentType.objects.get_for_model(self.__class__)
                    self.entity = Entity.objects.create(content_type=ct)
            result = super().save(*args, **kwargs)
            if created:
                self.refresh_from_db()  # need this to make sure that (self.entity.content_object == self) right away
            return result

    def delete(self, *args, **kwargs):
        """
        Permanently deletes the object by deleting its associated Entity.
        """
        return self.entity.delete(*args, **kwargs)

    def archive(self):
        """
        Soft-deletes the object by marking it `archived` and preventing the default `objects` Manager from accessing it.
        """
        return self.entity.archive()

    def restore(self):
        """
        Reverses the archiving or "soft-deletion" of the object and its Entity.
        """
        return self.entity.restore()

