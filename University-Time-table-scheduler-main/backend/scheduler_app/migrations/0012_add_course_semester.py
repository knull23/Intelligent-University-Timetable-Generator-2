# Generated manually to add semester field back to Course model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler_app', '0011_alter_course_course_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], default=1),
        ),
    ]
