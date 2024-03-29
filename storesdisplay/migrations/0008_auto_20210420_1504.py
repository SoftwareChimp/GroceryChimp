# Generated by Django 3.1.7 on 2021-04-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storesdisplay', '0007_auto_20210318_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoresdisplayStores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('nearby', models.IntegerField()),
            ],
            options={
                'db_table': 'storesdisplay_stores',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='StoresdisplayStore',
        ),
    ]
