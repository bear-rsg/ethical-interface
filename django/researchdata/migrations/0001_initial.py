# Generated by Django 4.2.14 on 2024-07-18 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_content', models.TextField()),
                ('response_required', models.BooleanField(default=False)),
                ('admin_approved', models.BooleanField(default=False)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(auto_now=True, verbose_name='last updated')),
            ],
            options={
                'ordering': ('-meta_created_datetime', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A research topic/theme that prompts are organised into.', max_length=255)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(auto_now=True, verbose_name='last updated')),
            ],
            options={
                'ordering': ('-meta_created_datetime', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_text', models.CharField(help_text="A word or phrase that will trigger a prompt to the user. Must match exactly to user's search term.", max_length=255)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(auto_now=True, verbose_name='last updated')),
            ],
            options={
                'ordering': ('-meta_created_datetime', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_content', models.TextField()),
                ('admin_approved', models.BooleanField(default=False)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='responses', to='researchdata.prompt')),
            ],
            options={
                'ordering': ['-meta_created_datetime'],
            },
        ),
        migrations.AddField(
            model_name='prompt',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='researchdata.topic'),
        ),
        migrations.AddField(
            model_name='prompt',
            name='triggers',
            field=models.ManyToManyField(related_name='prompts', to='researchdata.trigger'),
        ),
    ]
