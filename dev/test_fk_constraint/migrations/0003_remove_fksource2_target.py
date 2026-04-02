from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_fk_constraint', '0002_fksource1_target'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fksource2',
            name='target',
        ),
    ]
