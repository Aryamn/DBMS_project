from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	path('', auth_views.LoginView.as_view(template_name='user/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('upd_profile/', views.update, name='update')

]
