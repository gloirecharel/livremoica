from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views

app_name = 'users'  # Ajouté pour supporter les namespaces

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('books/', include(('books.urls', 'books'), namespace='books')),

    path('requests/', include(('bookrequests.urls', 'requests'), namespace='requests')),
]

urlpatterns += staticfiles_urlpatterns()
