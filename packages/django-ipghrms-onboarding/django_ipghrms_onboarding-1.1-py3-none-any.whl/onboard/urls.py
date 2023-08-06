from django.urls import path
from . import views

urlpatterns = [
	path('emp/list/', views.OnboardEmpList, name="onboard-emp-list"),
	path('emp/add/<str:hashid>/', views.OnboardEmpAdd, name="onboard-emp-add"),
	path('emp/lock/<str:hashid>/', views.OnboardEmpLock, name="onboard-emp-lock"),
	path('emp/unlock/<str:hashid>/', views.OnboardEmpUnLock, name="onboard-emp-unlock"),
	path('emp/finish/<str:hashid>/', views.OnboardEmpFinish, name="onboard-emp-finish"),
	#
	path('topic/list/<str:hashid>/', views.OnboardList, name="onboard-list"),
	path('topic/add/<str:hashid>/', views.OnboardAdd, name="onboard-add"),
	path('topic/update/<str:hashid>/<str:hashid2>/', views.OnboardUpdate, name="onboard-update"),
	path('topic/delete/<str:hashid>/<str:hashid2>/', views.OnboardDelete, name="onboard-delete"),
	#
	path('det/list/<str:hashid>/', views.OnboardDetList, name="onboard-det-list"),
	path('det/add/<str:hashid>/<str:page>/', views.OnboardDetAdd, name="onboard-det-add"),
	path('det/update/<str:hashid>/<str:hashid2>/<str:page>/', views.OnboardDetUpdate, name="onboard-det-update"),
	path('det/delete/<str:hashid>/<str:hashid2>/<str:page>/', views.OnboardDetDelete, name="onboard-det-delete"),
]