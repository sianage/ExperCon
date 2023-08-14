# Generated by Django 4.1.1 on 2023-05-28 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainApp', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='category',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='field',
            field=models.CharField(choices=[('philosophy', 'Philosophy'), ('economics', 'Economics'), ('medicine', 'Medicine'), ('political_science', 'Political Science')], default='No Field Selected', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
