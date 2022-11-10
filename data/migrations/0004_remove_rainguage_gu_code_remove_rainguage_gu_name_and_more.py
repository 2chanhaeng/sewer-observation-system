# Generated by Django 4.1.2 on 2022-11-09 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0003_gu_gubn"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rainguage",
            name="gu_code",
        ),
        migrations.RemoveField(
            model_name="rainguage",
            name="gu_name",
        ),
        migrations.RemoveField(
            model_name="sewer",
            name="gubn",
        ),
        migrations.RemoveField(
            model_name="sewer",
            name="gubn_nam",
        ),
        migrations.AlterField(
            model_name="gu",
            name="gubn",
            field=models.CharField(default="00", max_length=4, verbose_name="구분코드"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="rainguage",
            name="gu",
            field=models.ForeignKey(
                default=26,
                on_delete=django.db.models.deletion.CASCADE,
                to="data.gu",
                verbose_name="구청",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sewer",
            name="gu",
            field=models.ForeignKey(
                default=26,
                on_delete=django.db.models.deletion.CASCADE,
                to="data.gu",
                verbose_name="구청",
            ),
            preserve_default=False,
        ),
    ]
