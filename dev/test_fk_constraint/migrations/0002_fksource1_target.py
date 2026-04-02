from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_fk_constraint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fksource1',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_fk_constraint.fktarget'),
        ),
    ]
