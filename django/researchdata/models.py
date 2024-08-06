from django.db import models
import textwrap


class Topic(models.Model):
    """
    A research topic/theme that prompts are organised into
    """

    name = models.CharField(
        max_length=255,
        help_text="A research topic/theme that prompts are organised into."
    )

    admin_notes = models.TextField(blank=True, null=True)

    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="last updated")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-meta_created_datetime', 'id')


class Trigger(models.Model):
    """
    A word/phrase that a user searches for that triggers a prompt
    """

    trigger_text = models.CharField(
        max_length=255,
        help_text="A word or phrase that will trigger a prompt to the user. Must match exactly to user's search term."
    )

    admin_notes = models.TextField(blank=True, null=True)

    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="last updated")

    def __str__(self):
        return self.trigger_text

    class Meta:
        ordering = ('-meta_created_datetime', 'id')


class Prompt(models.Model):
    """
    A piece of information shown to users to prompt them to perform an action

    An action may be to submit a Response (see below model)
    or simply to read and think about information provided in this prompt
    """

    topic = models.ForeignKey(Topic, on_delete=models.RESTRICT)
    prompt_content = models.TextField()
    response_required = models.BooleanField(
        default=False,
        help_text="If you'd like the user to respond to this prompt via a text box, please tick this option."
    )

    triggers = models.ManyToManyField(Trigger, related_name='prompts')

    admin_approved = models.BooleanField(
        default=False,
        help_text="Only prompts that are approved will be publicly visible (e.g. feature in the web browser extension)."
    )
    admin_notes = models.TextField(blank=True, null=True)

    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="last updated")

    @property
    def prompt_content_preview(self):
        return textwrap.shorten(self.prompt_content, width=140, placeholder="...")

    def __str__(self):
        return f'Prompt #{self.id} - {str(self.meta_created_datetime)[:19]}: {textwrap.shorten(self.prompt_content, width=50, placeholder="...")}'

    class Meta:
        ordering = ('-meta_created_datetime', 'id')


class Response(models.Model):
    """
    The response that a user submits based on a prompt
    """

    prompt = models.ForeignKey(Prompt, related_name='responses', on_delete=models.PROTECT)
    response_content = models.TextField()

    admin_approved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, null=True)

    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="last updated")

    def __str__(self):
        return f'Response #{self.id} - {str(self.meta_created_datetime)[:19]}: {textwrap.shorten(self.response_content, width=50, placeholder="...")}'

    class Meta:
        ordering = ['-meta_created_datetime']
