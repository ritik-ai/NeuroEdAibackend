# Generated by Django 5.0.1 on 2024-08-21 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EducationAi', '0002_user_delete_requestuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]