# Generated by Django 4.1 on 2022-08-27 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='followers',
            constraint=models.UniqueConstraint(fields=('followed_by', 'following'), name='unique_following_index'),
        ),
        migrations.AddConstraint(
            model_name='followers',
            constraint=models.CheckConstraint(check=models.Q(('followed_by_id', models.F('following_id')), _negated=True), name='id_cant_be_the_same'),
        ),
    ]
