# Generated by Django 5.0.1 on 2024-08-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='requestuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=100)),
                ('user_password', models.TextField(max_length=50)),
                ('user_Address', models.TextField(max_length=50)),
                ('user_country', models.IntegerField()),
            ],
        ),
    ]
