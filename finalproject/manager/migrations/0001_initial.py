# Generated by Django 4.2.18 on 2025-02-16 21:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='boards_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status', to='manager.board')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('current_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='current_workflows', to='manager.status')),
                ('next_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='previous_workflows', to='manager.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ValueHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('field_name', models.CharField(max_length=255)),
                ('previous_value', models.CharField(max_length=255)),
                ('next_value', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_created', to=settings.AUTH_USER_MODEL)),
                ('current_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='manager.status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('value', models.CharField(max_length=255, null=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='filed_values', to='manager.field')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='filed_fields', to='manager.task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=500)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='manager.task')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
