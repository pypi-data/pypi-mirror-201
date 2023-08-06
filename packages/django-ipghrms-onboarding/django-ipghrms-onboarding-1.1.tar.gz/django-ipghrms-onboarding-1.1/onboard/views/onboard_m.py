import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from settings_app.decorators import allowed_users
from django.contrib import messages
from onboard.models import OnboardDet, OnboardEmp, Onboard
from onboard.forms import OnboardDetForm, OnboardForm
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardEmpAdd(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	newid, new_hashid = getnewid(Onboard)
	obj = OnboardEmp(id=newid, employee=emp,\
		user=request.user, datetime=datetime.datetime.now(), hashed=new_hashid)
	obj.save()
	messages.success(request, f'Onboarding created.')
	return redirect('onboard-list', hashid=new_hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardEmpLock(request, hashid):
	objects = get_object_or_404(OnboardEmp, hashed=hashid)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Xavi.')
	return redirect('onboard-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardEmpUnLock(request, hashid):
	objects = get_object_or_404(OnboardEmp, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Loke.')
	return redirect('onboard-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardEmpFinish(request, hashid):
	objects = get_object_or_404(OnboardEmp, hashed=hashid)
	objects.is_finish = True
	objects.save()
	messages.success(request, f'Termina.')
	return redirect('onboard-list', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardAdd(request, hashid):
	onboardemp = get_object_or_404(OnboardEmp, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Onboard)
		form = OnboardForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.onboardemp = onboardemp
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('onboard-list', hashid=hashid)
	else: form = OnboardForm()
	context = {
		'form': form, 'onboardemp': onboardemp, 'page': 'list',
		'title': 'Aumenta Topiku', 'legend': 'Aumenta Topiku'
	}
	return render(request, 'onboard/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardUpdate(request, hashid, hashid2):
	onboardemp = get_object_or_404(OnboardEmp, hashed=hashid)
	objects = get_object_or_404(Onboard, hashed=hashid2)
	if request.method == 'POST':
		form = OnboardForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('onboard-list', hashid=hashid)
	else: form = OnboardForm(instance=objects)
	context = {
		'onboardemp': onboardemp, 'objects': objects, 'form': form, 'page': 'list',
		'title': 'Altera Topiku', 'legend': 'Altera Topiku'
	}
	return render(request, 'onboard/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardDelete(request, hashid, hashid2):
	objects = get_object_or_404(Onboard, hashed=hashid2)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('onboard-list', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardDetAdd(request, hashid, page):
	onboard = get_object_or_404(Onboard, hashed=hashid)
	emp = onboard.onboardemp.employee
	if request.method == 'POST':
		newid, new_hashid = getnewid(OnboardDet)
		form = OnboardDetForm(emp, request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.onboard = onboard
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			if page == "topic": return redirect('onboard-list', hashid=onboard.onboardemp.hashed)
			else: return redirect('onboard-det-list', hashid=hashid)
	else: form = OnboardDetForm(emp)
	context = {
		'form': form, 'onboard': onboard, 'onboardemp': onboard.onboardemp, 'page': page,
		'title': 'Aumenta Materia', 'legend': 'Aumenta Materia'
	}
	return render(request, 'onboard/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardDetUpdate(request, hashid, hashid2, page):
	onboard = get_object_or_404(Onboard, hashed=hashid)
	objects = get_object_or_404(OnboardDet, hashed=hashid2)
	emp = onboard.onboardemp.employee
	if request.method == 'POST':
		form = OnboardDetForm(emp, request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			if page == "topic": return redirect('onboard-list', hashid=onboard.onboardemp.hashed)
			else: return redirect('onboard-det-list', hashid=hashid)
	else: form = OnboardDetForm(emp, instance=objects)
	context = {
		'onboard': onboard, 'onboardemp': onboard.onboardemp, 'objects': objects, 'form': form, 'page': 'det',
		'title': 'Altera Materia', 'legend': 'Altera Materia'
	}
	return render(request, 'onboard/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def OnboardDetDelete(request, hashid, hashid2, page):
	objects = get_object_or_404(OnboardDet, hashed=hashid2)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	if page == "topic": return redirect('onboard-list', hashid=objects.onboard.onboardemp.hashed)
	else: return redirect('onboard-det-list', hashid=hashid)

