# Generated by Django 3.2.1 on 2021-11-27 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0006_auto_20211127_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'permissions': [('export', 'Can export 应聘者 list'), ('notify', 'Can notify interviewer for candidate review')], 'verbose_name': '应聘者', 'verbose_name_plural': '应聘者'},
        ),
    ]
