# Generated by Django 5.1 on 2025-01-09 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0019_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='cc75bd', max_length=6),
        ),
    ]