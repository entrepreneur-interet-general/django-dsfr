# Generated by Django 3.2.9 on 2022-02-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_format',
            field=models.CharField(blank=True, choices=[('PAPER', 'Papier'), ('NUM', 'Numérique')], max_length=10, null=True, verbose_name='Format'),
        ),
    ]
