# Generated by Django 5.2.1 on 2025-05-17 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallBackRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('viewed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Заявка на обратный звонок',
                'verbose_name_plural': 'Заявки на обратный звонок',
                'ordering': ['-created_at'],
            },
        ),
    ]
