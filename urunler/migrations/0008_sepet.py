# Generated by Django 4.1.3 on 2023-02-19 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urunler', '0007_urun_olusturan_alter_urun_seri'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sepet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adet', models.IntegerField(default=1)),
                ('toplam', models.IntegerField()),
                ('odendiMi', models.BooleanField(default=False)),
                ('urun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urunler.urun')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
