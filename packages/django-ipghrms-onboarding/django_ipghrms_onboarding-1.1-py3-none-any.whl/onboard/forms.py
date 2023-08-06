from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from employee.models import Employee
from onboard.models import Onboard, OnboardDet
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
	input_type = 'date'

class OnboardForm(forms.ModelForm):
	class Meta:
		model = Onboard
		fields = ['topic']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('topic', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class OnboardDetForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(), required=False)
	comment = forms.CharField(label="Deskrisaun Detalha", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = OnboardDet
		fields = ['employee','subject','date','obs','execute','comment']
	def __init__(self, emp, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter().exclude(id=emp.id).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-4 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('obs', css_class='form-group col-md-2 mb-0'),
				Column('execute', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('subject', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)
