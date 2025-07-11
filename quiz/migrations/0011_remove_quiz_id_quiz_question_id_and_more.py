# Generated by Django 5.2 on 2025-04-21 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_studentinfo_std_roll_alter_studentinfo_no_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='id',
        ),
        migrations.AddField(
            model_name='quiz',
            name='question_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='std_roll',
            field=models.CharField(default=0),
        ),
        migrations.CreateModel(
            name='Test_quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=225)),
                ('std_name', models.CharField(max_length=225)),
                ('option_click', models.CharField(max_length=225)),
                ('question_id', models.ForeignKey(db_column='question_id_id', on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
            ],
        ),
    ]
