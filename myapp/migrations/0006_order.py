# Generated by Django 2.2.5 on 2019-10-02 18:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.IntegerField(choices=[(0, 'Purchase'), (1, 'Borrow')], default=1)),
                ('order_Date', models.DateField(default=django.utils.timezone.now)),
                ('books', models.ManyToManyField(blank=True, to='myapp.Book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='myapp.Member')),
            ],
        ),
    ]
