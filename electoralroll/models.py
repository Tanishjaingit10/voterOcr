from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        if self.city_name:
            return self.city_name
        else:
            return "-"

    class Meta:
        db_table = "cities"
        verbose_name_plural = "cities"


class LegislativeAssembly(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    assembly_name = models.CharField(max_length=25, null=False, blank=False)
    # submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.assembly_name:
            return self.assembly_name + " ---> " + self.city.city_name
        else:
            return "-"

    class Meta:
        db_table = "legislative_assembly"
        verbose_name_plural = "legislative_assemblies"

class PartNumber(models.Model):
    assembly = models.ForeignKey(LegislativeAssembly, on_delete=models.CASCADE)
    part_number = models.PositiveIntegerField()
    part_name = models.CharField(max_length=100, null=True, blank=True, default="-")
    part_location = models.CharField(max_length=100, null=True, blank=True, default="-")
    voter_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.assembly:
            return "Part "+ str(self.part_number) + " ---> " + self.assembly.assembly_name + " ---> " + self.assembly.city.city_name
        else:
            return "-"
    class Meta:
        db_table = "part_number"
        verbose_name_plural = "part_numbers"
        ordering = ["part_number"]

class Voter(models.Model):
    part = models.ForeignKey(PartNumber, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True, default="-")
    father_name = models.CharField(max_length=100, null=True, blank=True, default="-")
    husband_name = models.CharField(max_length=100, null=True, blank=True, default="-")
    house_no = models.CharField(max_length=25, null=True, blank=True, default="-")
    age = models.CharField(max_length=25, null=True, blank=True, default="-")
    UID = models.CharField(max_length=25, null=True, blank=True, default="-")
    Serial_no= models.PositiveIntegerField()
    anubhag=models.CharField(max_length=100,null=True,blank=True,default="-")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "voter"
        verbose_name_plural = "Voters"
        ordering = ["Serial_no"]
