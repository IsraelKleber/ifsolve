# Generated by Django 4.1.3 on 2023-01-07 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifsolve', '0009_alter_alternativa_justificativa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternativa',
            name='justificativa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alternativa',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
