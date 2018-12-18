# Generated by Django 2.1.2 on 2018-12-18 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False, verbose_name='email address')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='username')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('follower', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WeiboData',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('likes', models.IntegerField(default=0)),
                ('postData', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeiboLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('liker', models.CharField(max_length=100)),
            ],
        ),
    ]
