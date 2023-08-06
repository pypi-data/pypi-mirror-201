from django.contrib import admin

#from .indirect_inline import IndirectStackedInline
from django.contrib.contenttypes.admin import GenericStackedInline

from . import models

# Register your models here.

class EntityModelAdmin(admin.ModelAdmin):
    def get_inlines(self, request, obj):
        inlines = super().get_inlines(request, obj=obj)
        if EntityAdminInline not in inlines:
            return list(inlines) + [EntityAdminInline]
        return inlines

class EntityAdminInline(GenericStackedInline):
    model = models.Entity
    ct_fk_field = "id"
    extra = 3
    readonly_fields = ['id', 'content_type', 'domains', 'created_time', 'archived_time']
    fieldsets = (
        (None, {
            "fields": ('xattrs',)
        }),
        ("Timestamps", {
            "fields": ('created_time', 'archived_time'),
            "classes": ('collapse',),
        }),
        ("Advanced", {
            "fields": ('domains', 'content_type'),
            "classes": ('collapse',),
        })
    )

    def get_form_queryset(self, obj):
        return self.model.objects.filter(id=obj.entity_id)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    readonly_fields = ["content_type"]
    #inlines = [MembershipInline]
