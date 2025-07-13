from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('borrowed/', views.borrowed_index, name='borrowed'),  # ✅ ce nom est utilisé dans tes templates
    path('lent/', views.lent_index, name='lent'),              # ✅ idem
    path('accept/<int:id>/', views.accept, name='accept'),
    path('reject/<int:id>/', views.reject, name='reject'),
    path('return/<int:id>/', views.return_book, name='return'),
]
