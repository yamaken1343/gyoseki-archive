# Generated by Django 2.2.3 on 2019-09-05 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gyoseki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='recode',
            name='source',
        ),
        migrations.AddField(
            model_name='recode',
            name='en_journal',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='recode',
            name='en_place',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='recode',
            name='journal',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='recode',
            name='note',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='recode',
            name='place',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='recode',
            name='review',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recode',
            name='en_author',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='recode',
            name='en_title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.DeleteModel(
            name='Conf',
        ),
        migrations.AddField(
            model_name='recode',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gyoseki.Division'),
        ),
        migrations.AddField(
            model_name='recode',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='gyoseki.Tag'),
        ),
    ]
