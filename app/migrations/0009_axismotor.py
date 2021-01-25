# Generated by Django 3.1.5 on 2021-01-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210124_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='AxisMotor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('gpio_pin', models.IntegerField(unique=True)),
            ],
        ),
    ]
