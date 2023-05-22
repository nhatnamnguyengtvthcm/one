from django.contrib import admin

from one.libraries.utils.admin import GenericRelationAdmin, MasterModelAdmin

from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(GenericRelationAdmin, MasterModelAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets[0][1]["fields"] += (
            "content_type",
            "object_id",
            "is_active",
            "effective_date",
            "expiry_date",
            "allowance",
        )
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ("content_object", "effective_date", "expiry_date", "allowance")
