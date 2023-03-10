# Generated by Django 4.1.3 on 2022-11-17 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_spider_feeding_spider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='spider',
            name='decorations',
            field=models.ManyToManyField(to='main_app.decoration'),
        ),
    ]
