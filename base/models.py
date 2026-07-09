from django.db import models
from django.utils import timezone


class Operator(models.Model):
    name = models.CharField(max_length=100)
    token_id = models.CharField(max_length=20, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return self.name


class Machine(models.Model):
    machine_model = models.CharField(max_length=20)


    def __str__(self):
        return self.machine_model


class TimeStudy(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=50)
    operation = models.CharField(max_length=100)
    reading1 = models.FloatField(blank=True,null=True)
    reading2 = models.FloatField(blank=True,null=True)
    reading3 = models.FloatField(blank=True,null=True)
    reading4 = models.FloatField(blank=True,null=True)
    reading5 = models.FloatField(blank=True,null=True)
    average = models.FloatField(blank=True, null=True)
    allowance = models.FloatField()
    capacity = models.FloatField(blank=True,null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.operator.name} - {self.operation}"