from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from bookzilla import views

urlpatterns = [
    # index page
    re_path(r'^$', views.index, name='index'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^contact/$', views.contact, name='contact'),
    path('admin/', admin.site.urls),

    # the users module
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # courier module
    path('courier/', include(('courier.urls', 'courier'), namespace='courier')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
