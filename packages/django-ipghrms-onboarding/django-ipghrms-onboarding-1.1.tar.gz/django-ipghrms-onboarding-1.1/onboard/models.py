from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee

class Topik(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class OnboardEmp(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='onboardemp')
	is_active = models.BooleanField(default=True)
	is_lock = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee}'
		return template.format(self)

class Onboard(models.Model):
	onboardemp = models.ForeignKey(OnboardEmp, on_delete=models.CASCADE, related_name='onboard')
	topic = models.ForeignKey(Topik, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.onboardemp} - {0.topic}'
		return template.format(self)

class OnboardDet(models.Model):
	onboard = models.ForeignKey(Onboard, on_delete=models.CASCADE, related_name='onboarddet')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='onboarddet', verbose_name="Husi")
	subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Materia")
	date = models.DateField(null=True, blank=True)
	obs = models.CharField(choices=[('Yes','Yes'),('No','No')], max_length=3, null=True, blank=True)
	execute = models.CharField(max_length=200, null=True, blank=True, verbose_name="Executa")
	comment = models.TextField(null=True, blank=True, verbose_name="Komentariu")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.subject}'
		return template.format(self)
