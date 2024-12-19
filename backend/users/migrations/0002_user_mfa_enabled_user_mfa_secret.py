# Generated by Django 5.1.4 on 2024-12-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mfa_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='mfa_secret',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]