# Generated by Django 5.0.1 on 2024-08-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EducationAi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100, null=True)),
                ('user_password', models.CharField(max_length=50, null=True)),
                ('user_Address', models.CharField(max_length=50, null=True)),
                ('user_country', models.CharField(max_length=50, null=True)),
                ('user_plan', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='requestuser',
        ),
    ]
