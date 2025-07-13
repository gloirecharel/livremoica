from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from courier import views

app_name = 'courier'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^advance/(?P<req_id>\d+)/$', views.advance_request, name='advance'),
]

urlpatterns += staticfiles_urlpatterns()
