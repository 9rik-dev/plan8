# Generated by Django 3.2.9 on 2021-11-15 04:18

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import tasks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_manager', models.BooleanField(default=False, verbose_name='manager')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
            },
            managers=[
                ('objects', tasks.models.AccountManager()),
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
                ('developers', models.ManyToManyField(blank=True, related_name='developers', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ManyToManyField(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['creation_date'],
                'unique_together': {('title', 'description')},
            },
        ),
    ]
