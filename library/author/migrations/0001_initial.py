# Generated by Django 3.1.1 on 2021-03-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('surname', models.CharField(max_length=20, null=True)),
                ('patronymic', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
