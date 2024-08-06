from django.contrib import admin
from . import models


def approve(modeladmin, request, queryset):
    """
    Sets all selected items in queryset to approved
    """
    queryset.update(admin_approved=True)


approve.short_description = "Approve selected objects (will be publicly visible)"


def unapprove(modeladmin, request, queryset):
    """
    Sets all selected items in queryset to not approved
    """
    queryset.update(admin_approved=False)


unapprove.short_description = "Unapprove selected visions (will not be publicly visible)"


@admin.register(models.Topic)
class TopicAdminView(admin.ModelAdmin):
    """
    Customise the content of the list of Topics in the Django admin
    """
    list_display = ('id',
                    'name',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')
    list_per_page = 50


@admin.register(models.Trigger)
class TriggerAdminView(admin.ModelAdmin):
    """
    Customise the content of the list of Triggers in the Django admin
    """
    list_display = ('id',
                    'trigger_text',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')
    list_per_page = 50


@admin.register(models.Prompt)
class PromptAdminView(admin.ModelAdmin):
    """
    Customise the content of the list of Prompts in the Django admin
    """
    list_display = ('id',
                    'topic',
                    'prompt_content',
                    'response_required',
                    'admin_approved',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')
    list_filter = ('admin_approved',)
    list_per_page = 50
    actions = (approve, unapprove)


@admin.register(models.Response)
class ResponseAdminView(admin.ModelAdmin):
    """
    Customise the content of the list of Prompts in the Django admin
    """
    list_display = ('id',
                    'response_content',
                    'prompt',
                    'admin_approved',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')
    list_filter = ('admin_approved',)
    list_per_page = 50
    actions = (approve, unapprove)
