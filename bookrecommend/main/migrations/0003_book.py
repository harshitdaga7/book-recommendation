# Generated by Django 3.2 on 2021-04-16 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userinfo_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('category', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=1000)),
            ],
        ),
    ]
