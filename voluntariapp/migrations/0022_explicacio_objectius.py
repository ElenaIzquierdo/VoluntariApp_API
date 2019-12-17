# Generated by Django 3.0 on 2019-12-16 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voluntariapp', '0021_centreinteres_cours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objectius',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('centreinteres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voluntariapp.CentreInteres')),
            ],
        ),
        migrations.CreateModel(
            name='Explicacio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True)),
                ('description', models.TextField()),
                ('centreinteres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voluntariapp.CentreInteres')),
            ],
        ),
    ]
