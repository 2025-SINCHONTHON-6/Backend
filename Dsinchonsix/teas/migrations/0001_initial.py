import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeaCategory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10, verbose_name='카테고리 이름')),
                ('mood', models.CharField(max_length=20, verbose_name='기분 이름')),
            ],
        ),
        migrations.CreateModel(
            name='Tea',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10, verbose_name='차 이름')),
                ('description', models.TextField(verbose_name='차 설명')),
                ('taste', models.CharField(max_length=30, verbose_name='차 맛')),
                ('tea_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teas.teacategory', verbose_name='카테고리 종류')),
            ],
        ),
    ]
