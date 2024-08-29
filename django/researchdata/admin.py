from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
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


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """

    list_per_page = 50
    search_fields = (
        'id',
        'name',
        'meta_created_datetime',
        'meta_lastupdated_datetime'
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


# Simple models that extend GenericAdminViews without changes
admin.site.register(models.TopicGroup, GenericAdminView)
admin.site.register(models.Topic, GenericAdminView)


@admin.register(models.Trigger)
class TriggerAdminView(GenericAdminView):
    """
    Customise the content of the list of Triggers in the Django admin
    """
    list_display = ('id',
                    'trigger_text',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')


@admin.register(models.Prompt)
class PromptAdminView(GenericAdminView):
    """
    Customise the content of the list of Prompts in the Django admin
    """
    list_display = ('id',
                    'topic',
                    'prompt_content',
                    'response_required',
                    'priority',
                    'admin_approved',
                    'meta_created_datetime',
                    'meta_lastupdated_datetime')
    list_filter = ('admin_approved',)
    actions = (approve, unapprove)


@admin.register(models.Response)
class ResponseAdminView(GenericAdminView):
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
    actions = (approve, unapprove)
