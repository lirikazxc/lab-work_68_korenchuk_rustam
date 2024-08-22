from django.urls import path
from calculator import views
from calculator.views import IndexView

urlpatterns = [
    path('add/', views.add),
    path('subtract/', views.subtract),
    path('multiply/', views.multiply),
    path('divide/', views.divide),
    path('index/', IndexView.as_view(), name='index'),

]