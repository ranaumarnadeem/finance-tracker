from django.db import models

class DebtEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_incurred = models.DateField()
    checkbox = models.BooleanField(default=False)
