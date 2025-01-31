# Generated by Django 2.0.3 on 2019-01-07 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('event', models.CharField(max_length=500, unique=True)),
                ('date_of_event', models.DateTimeField(verbose_name='Date of Event:')),
                ('event_notes', models.TextField(blank=True, null=True, verbose_name='Notes, Details, Production Team, Phone Numbers etc.')),
                ('is_archived', models.BooleanField(default=False, verbose_name='Archived')),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venues.Venue')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
