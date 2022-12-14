# Generated by Django 4.1.3 on 2022-11-09 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=8, verbose_name="구청명")),
                ("code", models.SmallIntegerField(verbose_name="구청 코드")),
            ],
        ),
        migrations.AlterField(
            model_name="rainguage",
            name="gu_code",
            field=models.SmallIntegerField(null=True, verbose_name="구청 코드"),
        ),
        migrations.AlterField(
            model_name="rainguage",
            name="gu_name",
            field=models.CharField(max_length=8, null=True, verbose_name="구청명"),
        ),
        migrations.AlterField(
            model_name="sewer",
            name="gubn",
            field=models.CharField(max_length=4, null=True, verbose_name="구분코드"),
        ),
        migrations.AlterField(
            model_name="sewer",
            name="gubn_nam",
            field=models.CharField(max_length=4, null=True, verbose_name="구분명"),
        ),
        migrations.AddField(
            model_name="rainguage",
            name="gu",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="data.gu",
                verbose_name="구청",
            ),
        ),
        migrations.AddField(
            model_name="sewer",
            name="gu",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="data.gu",
                verbose_name="구청",
            ),
        ),
    ]
