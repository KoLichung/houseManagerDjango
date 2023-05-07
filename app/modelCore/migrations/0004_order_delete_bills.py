# Generated by Django 4.2 on 2023-05-07 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0003_alter_user_about_me_alter_user_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('UNPAID', '未付款'), ('PAID', '已付款')], default='UNPAID', max_length=20)),
                ('price', models.IntegerField(default=0)),
                ('time_period', models.IntegerField(default=0)),
                ('pay_date', models.DateField(null=True)),
                ('expire_date', models.DateField(null=True)),
                ('plan', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('auth_code', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('card4no', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('card6no', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('CustomField1', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('ExecTimes', models.IntegerField(default=0)),
                ('Frequency', models.IntegerField(default=0)),
                ('gwsr', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('MerchantID', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('MerchantTradeNo', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('PaymentDate', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('PaymentType', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('PaymentTypeChargeFee', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('PeriodAmount', models.IntegerField(default=0)),
                ('PeriodType', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('process_date', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('RtnCode', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('RtnMsg', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('SimulatePaid', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('TotalSuccessAmount', models.IntegerField(default=0)),
                ('TotalSuccessTimes', models.IntegerField(default=0)),
                ('TradeAmt', models.IntegerField(default=0)),
                ('TradeDate', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('TradeNo', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('CheckMacValue', models.CharField(blank=True, default='', max_length=125, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Bills',
        ),
    ]
