# Generated by Django 4.0.2 on 2022-02-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0010_alter_book_checkin_alter_book_checkout_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='code',
            field=models.CharField(default='40A9M6R8', max_length=8, null=True),
        ),
    ]
