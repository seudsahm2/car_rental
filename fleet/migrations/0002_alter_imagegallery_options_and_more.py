# Generated by Django 5.2.3 on 2025-06-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagegallery',
            options={'ordering': ['-is_primary', 'order']},
        ),
        migrations.RenameField(
            model_name='imagegallery',
            old_name='is_featured',
            new_name='is_primary',
        ),
        migrations.RemoveField(
            model_name='car',
            name='image_path',
        ),
        migrations.AlterField(
            model_name='imagegallery',
            name='image_path',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddConstraint(
            model_name='imagegallery',
            constraint=models.UniqueConstraint(condition=models.Q(('is_primary', True)), fields=('car', 'is_primary'), name='unique_primary_image_per_car'),
        ),
    ]
