import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import onboard
from onboard.models import Onboard, OnboardDet, OnboardEmp
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from employee.models import CurEmpDivision, CurEmpPosition, Employee, FIDNumber, Photo
from onboard.models import OnboardEmp, Onboard

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def OnboardEmpList(request):
	group = request.user.groups.all()[0].name
	objects = []
	emps = Employee.objects.all().order_by('first_name')
	for i in emps:
		a = OnboardEmp.objects.filter(employee=i).first()
		b = False
		if a:
			b = True
		objects.append([i,a,b])
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Funsionario/a ho Status Onboard', 'legend': 'Lista Funsionario/a ho Status Onboard'
	}
	return render(request, 'onboard/emp_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def OnboardList(request, hashid):
	group = request.user.groups.all()[0].name
	onboardemp = get_object_or_404(OnboardEmp, hashed=hashid)
	emp = onboardemp.employee
	img = Photo.objects.get(employee=emp)
	onboards = Onboard.objects.filter(onboardemp=onboardemp).all()
	objects = []
	for i in onboards:
		a = OnboardDet.objects.filter(onboard=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'onboardemp': onboardemp, 'emp': emp, 'objects': objects, 'img': img, 'page': 'topic',
		'title': 'Informasaun Onboarding Pessoal', 'legend': 'Informasaun Onboarding Pessoal'
	}
	return render(request, 'onboard/topic_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def OnboardDetList(request, hashid):
	group = request.user.groups.all()[0].name
	onboard = get_object_or_404(Onboard, hashed=hashid)
	onboardemp = onboard.onboardemp
	objects = OnboardDet.objects.filter(onboard=onboard).all()
	context = {
		'group': group, 'onboard': onboard, 'objects': objects, 'onboardemp': onboardemp, 'page': 'dept',
		'title': 'Lista Materia', 'legend': 'Lista Materia'
	}
	return render(request, 'onboard/det_list.html', context)
