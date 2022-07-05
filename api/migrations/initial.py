from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.migration):
    
        dependencies = [
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ]
    
        operations = [
            migrations.CreateModel(
                name='Clubs',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=100)),
                    ('description', models.TextField(max_length=1e4)),
                    ('adminRollNo', models.CharField(max_length=9)),
                    ('image', models.ImageField(upload_to='images/', default='images/default.png')),
                    ('logo', models.ImageField(upload_to='logos/', default='logos/default.png')),
                    ('projects', models.ManyToManyField(to='api.Projects', blank=True)),
                    ('members', models.ManyToManyField(to='api.Members', blank=True)),
                    ('links', models.CharField(max_length=100)),
                    ('updated_at', models.DateTimeField(auto_now=True)),
                ],
            ),
            migrations.CreateModel(
                name='Members',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=100)),
                    ('rollNo', models.CharField(max_length=9)),
                    ('image', models.ImageField(upload_to='images/', default='images/default.png')),
                    # ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Clubs')),
                    # ('projects', models.ManyToManyField(to='api.Projects', blank=True)),
                    # ('links', models.CharField(max_length=100)),
                    ('updated_at', models.DateTimeField(auto_now=True)),
                ],
            ),
            migrations.CreateModel( 
                name='Projects',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=100)),
                    ('description', models.TextField(max_length=1e4)),
                    ('image', models.ImageField(upload_to='images/', default='images/default.png')),
                    ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Clubs')),
                    ('members', models.ManyToManyField(to='api.Members', blank=True)),
                    ('links', models.CharField(max_length=100)),
                    ('updated_at', models.DateTimeField(auto_now=True)),
                ]
            )
        ]
