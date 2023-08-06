from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoBaseUserAdmin

from onto.admin import EntityModelAdmin

from . import models

# Register your models here.

class BaseUserAdmin(EntityModelAdmin, DjangoBaseUserAdmin):
    # Swap first_name and last_name with display_name
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        list_display.insert(list_display.index("first_name"), "display_name")
        list_display.remove("first_name")
        list_display.remove("last_name")
        return list_display

    def get_fieldsets(self, request, obj):
        fieldsets = super().get_fieldsets(request, obj)
        for section, content in fieldsets:
            if section == "Personal info":
                content["fields"] = ("display_name", "email")
        return fieldsets
        
@admin.register(models.Policy)
class PolicyAdmin(admin.ModelAdmin):
    filter_horizontal = ["actions"]

@admin.register(models.Domain)
class DomainAdmin(EntityModelAdmin):
    filter_horizontal = ["entities"]
    search_fields = ['name']