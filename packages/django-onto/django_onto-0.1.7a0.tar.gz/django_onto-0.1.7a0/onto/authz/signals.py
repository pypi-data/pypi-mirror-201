"""
onto Authz uses many (optional) signals to automate Entitlement management. This is crucial for keeping distributed authorization systems in sync.

For example, changing the `xattrs` or `domains` of an Entity may change which Policies apply to it, which may need to be communicated to a remote authorization system.
This is all automated here, more or less with running as few queries as possible while keeping a distributed system consistent!
"""
from collections import namedtuple
from functools import cache

from django.db.models import Q, signals
from django.dispatch import Signal, receiver

import onto.authz.models
import onto.models

audit_log = onto.authz.models.audit_log

entitlement_enabled = Signal()
entitlement_disabled = Signal()

class silent_entitlements:
    """
    Context manager that suppresses `entitlement_enabled` and `entitlement_disabled` signals from firing within the scope.

    Primarily useful for "reverse-synchronizing" the database with a remote system, as a one-off or infrequent procedure.

    >>> with silent_entitlements():
    ...     # This won't cause any of the above signals to fire
    ...     something_that_affects_entitlements()
    
    """
    active = False
    def __enter__(self):
        silent_entitlements.active = True
    def __exit__(self, type, value, traceback):
        silent_entitlements.active = False


@receiver(signals.post_save, sender=onto.authz.models.Entitlement)
def on_entitlement_save(instance, sender,**kwargs):
    """
    When an Entitlement is saved, if its the only one of its kind, emit an `entitlement_enabled` signal.
    """
    print("on_entitlement_save", instance)
    audit_log.info(f"ENTITLEMENT ADDED {instance.principal} {instance.action.label} {instance.resource} (policy: {instance.policy})")

    if not silent_entitlements.active and not instance.peers.exists():  # TODO Verify this won't race.
        audit_log.info(f"ENABLED {instance.principal} {instance.action.label} {instance.resource} (first entitlement gained)")
        entitlement_enabled.send(
            sender=sender,
            principal=instance.principal,
            action=instance.action,
            resource=instance.resource,
            )

@receiver(signals.post_delete, sender=onto.authz.models.Entitlement)
def on_entitlement_delete(instance, sender, **kwargs):
    """
    When an Entitlement is deleted, if it was the only one of its kind, emit an `entitlement_disabled` signal.
    """
    print("on_entitlement_delete", instance)
    audit_log.info(f"ENTITLEMENT REMOVED {instance.principal} {instance.action.label} {instance.resource} (policy: {instance.policy})")

    if not silent_entitlements.active and not instance.peers.exists():
        audit_log.info(f"DISABLED {instance.principal} {instance.action.label} {instance.resource} (no entitlements remaining)")
        entitlement_disabled.send(
            sender=sender,
            principal=instance.principal,
            action=instance.action,
            resource=instance.resource,
            )

@receiver(signals.post_save, sender=onto.authz.models.Action)
def on_action_save(**kwargs):
    get_dispatching_actions.cache_clear()
    get_affected_types.cache_clear()

@cache
def get_dispatching_actions():
    return set(onto.authz.models.Action.objects.filter(dispatch_changes=True))

@cache
def get_affected_types():
    actions = get_dispatching_actions()
    return {action.source_type for action in actions}.union({action.target_type for action in actions})

#
# Below are various receivers to support the automation of Entitlement management
#
Policies = namedtuple('Policies', ('as_principal', 'as_resource'))

def evaluate_policies(instance: onto.models.Entity, past_policies: Policies, domains=None):
    print("evaluate_policies", instance)
    # A user or access-controlled Entity had changes to its security attributes, so reevaluate Policies.
    # First recompile Entitlements where the instance is a Principal
    domains = domains or instance.domains.filter(active=True)
    potential_policies = onto.authz.models.Policy.objects.filter(domain__in=domains, actions__source_type=instance.content_type)
    matching_policies = {policy for policy in potential_policies if policy.principals.filter(pk=instance.pk).exists()}
    previous_matching_policies = set(past_policies.as_principal)

    for new_policy in matching_policies - previous_matching_policies:
        # create entitlements with instance as target resource
        for action in new_policy.actions.filter(source_type=instance.content_type, dispatch_changes=True):
            for resource in new_policy.resources:
                action.entitlements.create(
                    domain=new_policy.domain,
                    policy=new_policy,
                    principal=instance,
                    resource=resource,
                )
    for old_policy in previous_matching_policies - matching_policies:
        old_policy.entitlements.filter(principal=instance).delete()

    # Now recompile Entitlements where the instance is a target Resource
    potential_policies = onto.authz.models.Policy.objects.filter(domain__in=instance.domains.filter(active=True), actions__target_type=instance.content_type)
    matching_policies = {policy for policy in potential_policies if policy.resources.filter(pk=instance.pk).exists()}
    previous_matching_policies = set(past_policies.as_resource)

    for new_policy in matching_policies - previous_matching_policies:
        # create entitlements with instance as target resource
        for action in new_policy.actions.filter(target_type=instance.content_type, dispatch_changes=True):
            for principal in new_policy.principals:
                action.entitlements.create(
                    domain=new_policy.domain,
                    policy=new_policy,
                    principal=principal,
                    resource=instance,
                )
    for old_policy in previous_matching_policies - matching_policies:
        old_policy.entitlements.filter(resource=instance).delete()


@receiver(signals.pre_save, sender=onto.models.Entity)
def before_entity_save(instance, sender, **kwargs):
    """
    Before an Entity is saved, check if its `xattrs` was modified, so we can update Entitlements later.
    """
    print("before_entity_save", instance)
    if instance.content_type not in get_affected_types():
        return
    try:
        db_instance = sender.objects_archive.get(pk=instance.pk)
        if instance.xattrs != db_instance.xattrs:
            instance._db_policies = Policies(
                as_principal=onto.authz.models.Policy.objects.filter(entitlements__principal=db_instance).distinct(),
                as_resource=onto.authz.models.Policy.objects.filter(entitlements__resource=db_instance).distinct(),
            )
    except sender.DoesNotExist:  # New Entity
        instance._db_policies = Policies(
            as_principal=onto.authz.models.Policy.objects.none(),
            as_resource=onto.authz.models.Policy.objects.none(),
        )


@receiver(signals.post_save, sender=onto.models.Entity)
def after_entity_save(instance, sender, **kwargs):
    """
    After an Entity is saved, if its security attributes were modified, create/delete Entitlements accordingly.
    """
    print("after_entity_save", instance)
    if getattr(instance, "_db_policies", None):
        evaluate_policies(instance, instance._db_policies)
        delattr(instance, "_db_policies")


def on_membership_added(domain, entity):
    print("on_membership_added", domain, entity)
    if not domain.active:
        return

    actions = onto.authz.models.Action.objects.filter(dispatch_changes=True)

    # Create principal entitlements for any dispatching actions that apply to this entity
    for action in actions.filter(source_type=entity.content_type):
        for resource in domain.entities.filter(content_type=action.target_type, restricted=False):
            action.entitlements.create(
                domain=domain,
                principal=entity,
                resource=resource,
                policy=None,
            )
    # Create target resource entitlements for any dispatching actions that apply to this entity
    for action in actions.filter(target_type=entity.content_type):
        for principal in domain.entities.filter(content_type=action.source_type, restricted=False):
            action.entitlements.create(
                domain=domain,
                principal=principal,
                resource=entity,
                policy=None,
            )

def on_membership_removed(domain, entity):
    print("on_membership_removed", domain, entity)
    domain.entitlements.filter(Q(principal=entity)|Q(resource=entity)).delete()

@receiver(signals.pre_save, sender=onto.authz.models.Membership)
def before_membership_save(instance, sender, **kwargs):
    """
    Before a Membership is saved, check if its `xattrs` was modified, so we can update the associated Entity's Entitlements later.
    """
    print("before_membership_save", instance)
    try:
        db_instance = sender.objects.get(pk=instance.pk)
        if instance.xattrs == db_instance.xattrs:
            return
    except sender.DoesNotExist:  # New Membership -- handled by `after_membership_save`
        pass

    instance.entity._db_policies = Policies(
        as_principal=onto.authz.models.Policy.objects.filter(entitlements__principal=instance.entity).distinct(),
        as_resource=onto.authz.models.Policy.objects.filter(entitlements__resource=instance.entity).distinct(),
    )

@receiver(signals.post_save, sender=onto.authz.models.Membership)
def after_membership_save(instance, sender, created, **kwargs):
    """
    After an Membership is saved, if its extended attributes were modified, create/delete Entitlements accordingly for its associated Entity.
    """
    print("after_membership_save", instance)
    domain = instance.domain
    entity = instance.entity

    if created:
        on_membership_added(domain, entity)

    if getattr(entity, "_db_policies", None):
        evaluate_policies(entity, entity._db_policies, domains=(domain,))
        delattr(entity, "_db_policies")


@receiver(signals.post_delete, sender=onto.authz.models.Membership)
def after_membership_delete(instance, sender, **kwargs):
    """
    After an Membership is saved, clean up any corresponding Entitlements.
    """
    print("after_membership_delete", instance)
    on_membership_removed(instance.domain, instance.entity)

@receiver(signals.pre_save, sender=onto.authz.models.Policy)
def before_policy_save(instance, sender, **kwargs):
    """
    Before a Policy is changed, identify any changes in the filters.
    """
    print("before_policy_save", instance)
    try:
        db_instance = sender.objects.get(pk=instance.pk)
        if instance.principal_filters != db_instance.principal_filters:
            instance._db_principals = set(db_instance.principals)
        if instance.resource_filters != db_instance.resource_filters:
            instance._db_resources = set(db_instance.resources)
    except sender.DoesNotExist:
        instance._db_principals = set()
        instance._db_resources = set()


@receiver(signals.post_save, sender=onto.authz.models.Policy)
def after_policy_save(instance, created, sender, **kwargs):
    """
    After a Policy is saved, if its filters were changed, adjust associated Entitlements accordingly.
    """
    print("after_policy_save", instance)
    if not created and (instance.disabled or not instance.domain.active):
        return instance.entitlements.all().delete()

    if getattr(instance, "_db_principals", False):
        # Principal filters were changed
        principals = set(instance.principals)
        for new_principal in principals - instance._db_principals:
            for action in instance.actions.filter(source_type=new_principal.content_type):
                for resource in instance.resources:
                    action.entitlements.create(
                        domain=instance.domain,
                        policy=instance,
                        principal=new_principal,
                        resource=resource,
                    )
        for old_principal in instance._db_principals - principals:
            instance.entitlements.filter(principal=old_principal).delete()
        delattr(instance, "_db_resources")

    if getattr(instance, "_db_resources", False):
        resources = set(instance.resources)
        for new_resource in resources - instance._db_resources:
            for action in instance.actions.filter(target_type=new_resource.content_type):
                for principal in instance.principals:
                    action.entitlements.create(
                        domain=instance.domain,
                        policy=instance,
                        principal=principal,
                        resource=new_resource,
                    )
        for old_resource in instance._db_resources - resources:
            instance.entitlements.filter(resource=old_resource).delete()
        delattr(instance, "_db_resources")


@receiver(signals.m2m_changed, sender=onto.authz.models.Policy.actions.through)
def on_policy_action_change(action, instance, pk_set, **kwargs):
    print("on_policy_action_change", instance)
    change_type = action; del action  # 'action' param is Django's not ours, so let's fix that for clarity.

    if change_type not in ("post_add", "post_remove",):  # post_clear?
        return
    if isinstance(instance, onto.authz.models.Policy):
        policies = [instance]
        actions = onto.authz.models.Action.objects.filter(pk__in=pk_set)
    else:
        actions = [instance]
        policies = onto.authz.models.Policy.objects.filter(pk__in=pk_set)

    for policy in policies:
        if change_type == "post_remove":
            policy.entitlements.filter(action__in=actions).delete()
        elif change_type == "post_add":
            for action in actions:
                for resource in policy.resources.filter(content_type=action.target_type):
                    for principal in policy.principals.filter(content_type=action.source_type):
                        action.entitlements.create(
                            domain=policy.domain,
                            policy=policy,
                            principal=principal,
                            resource=resource,
                        )


@receiver(signals.m2m_changed, sender=onto.models.Entity.domains.through)
def on_domain_entities_change(action, instance, pk_set, **kwargs):
    """
    When an Entity is added or removed from a Domain, we create or delete Entitlements accordingly.
    """
    print("on_domain_entities_change", instance)
    change_type = action; del action  # 'action' param is Django's not ours, so let's fix that for clarity.
    if change_type not in ("post_add", "post_remove",):  # post_clear?
        return

    if isinstance(instance, onto.authz.models.Domain):
        domains = [instance] if instance.active else []
        entities = onto.models.Entity.objects.filter(pk__in=pk_set, content_type__in=get_affected_types())
    elif instance.content_type in get_affected_types():
        entities = [instance]
        domains = onto.authz.models.Domain.objects.filter(pk__in=pk_set, active=True)
    else:
        return

    for domain in domains:
        for entity in entities:
            if change_type == "post_add":
                on_membership_added(domain, entity)

            elif change_type == "post_remove":
                on_membership_removed(domain, entity)

@receiver(signals.post_save, sender=onto.authz.models.Domain)
def on_domain_saved(instance, created, **kwargs):
    print("on_domain_saved", instance)
    if not instance.active and not created:
        instance.entitlements.all().delete()