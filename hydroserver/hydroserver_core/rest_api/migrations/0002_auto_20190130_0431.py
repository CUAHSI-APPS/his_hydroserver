# Generated by Django 2.1.5 on 2019-01-30 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('network_id', models.TextField(unique=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.RenameField(
            model_name='database',
            old_name='collection_id',
            new_name='network_id',
        ),
        migrations.AlterField(
            model_name='database',
            name='database_id',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='database',
            unique_together={('network_id', 'database_id')},
        ),
    ]