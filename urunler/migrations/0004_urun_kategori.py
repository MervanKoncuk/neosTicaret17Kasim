# Generated by Django 4.1.3 on 2023-01-17 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0003_kategori'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='kategori',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='urunler.kategori'),
        ),
    ]
