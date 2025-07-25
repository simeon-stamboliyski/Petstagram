# Generated by Django 4.2.21 on 2025-07-19 14:58

from django.db import migrations, models
import petstagram.photos.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images', validators=[petstagram.photos.validators.validate_file_size])),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('date_of_publication', models.DateTimeField(auto_now=True)),
                ('tagged_pets', models.ManyToManyField(blank=True, to='pets.pet')),
            ],
        ),
    ]
