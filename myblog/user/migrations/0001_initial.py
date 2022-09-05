# Generated by Django 4.0.4 on 2022-05-16 10:29

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(db_index=True, max_length=11, unique=True, verbose_name='昵称')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('sign', models.CharField(default=user.models.default_sign, max_length=32, verbose_name='个性签名')),
                ('avatar', models.ImageField(null=True, upload_to='avatar')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='电话号码')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]