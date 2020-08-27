# Generated by Django 3.1 on 2020-08-27 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
    ]