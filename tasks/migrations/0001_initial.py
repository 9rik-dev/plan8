# Generated by Django 3.2.9 on 2021-11-13 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True, db_index=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('developing', 'Developing'), ('review', 'Review'), ('closed', 'Closed')], default='open', max_length=10)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=10)),
                ('rejected', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.manager')),
            ],
            options={
                'ordering': ['creation_date'],
                'unique_together': {('title', 'description')},
            },
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.task')),
            ],
        ),
    ]
