# Generated by Django 3.1.5 on 2021-01-06 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20210106_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='script',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.script'),
        ),
    ]
