# Generated by Django 5.0.7 on 2024-07-31 15:53

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(100000)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_sessions', to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_sessions', to='quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='SessionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='quiz_session.quizsession')),
            ],
            options={
                'unique_together': {('session', 'name')},
            },
        ),
    ]