from django.db import models


class FKTarget(models.Model):
    """Target model for foreign key references"""

    name = models.CharField(max_length=50)


class FKSource1(models.Model):
    """Sequential migrations with foreign key field"""

    # Changing history
#    field1 = models.CharField(max_length=10)  # 0001
    field1 = models.CharField(max_length=10)  # 0002
    target = models.ForeignKey(FKTarget, on_delete=models.CASCADE, null=True)  # 0002


class FKSource2(models.Model):
    """Sequential migrations adding then removing a foreign key"""

    # Changing history
#    field1 = models.CharField(max_length=10)  # 0001
#    target = models.ForeignKey(FKTarget, on_delete=models.CASCADE, null=True)  # 0001
    field1 = models.CharField(max_length=10)  # 0003
    # no target  # 0003
