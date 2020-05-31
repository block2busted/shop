# Generated by Django 3.0.6 on 2020-05-31 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_auto_20200531_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(help_text='город', max_length=100)),
                ('street', models.CharField(help_text='улица', max_length=100)),
                ('home', models.CharField(help_text='дом', max_length=100)),
                ('flat', models.CharField(help_text='квартира', max_length=100)),
                ('first_name', models.CharField(help_text='имя', max_length=100)),
                ('last_name', models.CharField(help_text='Фамилия', max_length=100)),
                ('phone', models.CharField(help_text='Телефон', max_length=100)),
                ('email', models.CharField(help_text='Почта', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
        migrations.AddField(
            model_name='order',
            name='order_detail',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.OrderDetail'),
        ),
    ]
