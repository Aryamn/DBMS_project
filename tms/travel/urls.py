from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [

	path('', views.home, name='home'),
	path('addtrip/', views.addtrip, name='addtrip')
    # path('logout/', views.logout, name='logout'),
    # path('signup/', views.register, name='signup'),
    # path('profile/', views.profile, name='profile')

]