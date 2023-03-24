# Generated by Django 4.1.7 on 2023-03-24 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='passbookInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_created_date', models.DateField(auto_created=True, auto_now_add=True)),
                ('particular', models.CharField(max_length=100)),
                ('debit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=14)),
                ('credit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=14)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20)),
            ],
        ),
    ]
