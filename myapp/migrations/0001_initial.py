# Generated by Django 3.2.7 on 2021-11-11 02:34

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
            name='item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=255)),
                ('display', models.BooleanField(default=True)),
                ('images', models.ImageField(null=True, upload_to='images/')),
                ('harga', models.IntegerField()),
                ('luas', models.IntegerField()),
                ('lokasi', models.CharField(max_length=100)),
                ('keunikan', models.CharField(blank=True, max_length=100, null=True)),
                ('aksesair', models.CharField(blank=True, max_length=100, null=True)),
                ('sertifikasi', models.CharField(blank=True, max_length=100, null=True)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('dateupdated', models.DateTimeField(auto_now=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userpic', models.ImageField(blank=True, default='default.png', null=True, upload_to='profile/')),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
                ('headline', models.CharField(blank=True, max_length=255, null=True)),
                ('products', models.ManyToManyField(to='myapp.item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='personaldata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(blank=True, max_length=15, null=True)),
                ('nowa', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('pob', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]