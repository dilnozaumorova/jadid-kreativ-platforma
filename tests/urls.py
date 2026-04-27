from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('take/<int:test_id>/', views.submit_test, name='submit_test'),
    path('result/<int:result_id>/', views.test_result, name='test_result'),
]
