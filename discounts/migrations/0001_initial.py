# Generated by Django 3.2 on 2022-07-23 08:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('kind', models.CharField(choices=[('percent', 'Percentage'), ('amount', 'Amount')], max_length=10, verbose_name='Kind')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Code')),
                ('percentage', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Percentage')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('used_by', models.ManyToManyField(blank=True, editable=False, to=settings.AUTH_USER_MODEL, verbose_name='Used by')),
            ],
            options={
                'verbose_name': 'Discount code',
                'verbose_name_plural': 'Discount codes',
                'ordering': ('-created',),
            },
        ),
    ]
