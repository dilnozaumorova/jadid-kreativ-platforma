from django.urls import path
from . import views

app_name = 'moduls'

urlpatterns = [
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('lecture/<int:pk>/', views.lecture_detail, name='lecture_detail'),
    path('lecture/<int:lecture_id>/submit/', views.submit_lecture_test, name='submit_lecture_test'),
    path('lecture/<int:lecture_id>/retake/', views.retake_lecture_test, name='retake_lecture_test'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/submit/', views.submit_task, name='submit_task'),
    path('normative-documents/', views.normative_documents_list, name='normative_documents_list'),
    path('resources/', views.resource_list, name='resource_list'),
    path('creative-tasks/', views.creative_tasks, name='creative_tasks'),
    path('creative-tasks/<int:pk>/', views.creative_task_detail, name='creative_task_detail'),
    path('practice/', views.practice_list, name='practice_list'),
    path('practice/<int:pk>/', views.practice_detail, name='practice_detail'),
    path('practice/question/<int:pk>/', views.practice_question_detail, name='practice_question_detail'),
    path('table-practice/<int:pk>/', views.table_practice_detail, name='table_practice_detail'),
    path('seminars/', views.seminar_list, name='seminar_list'),
    path('seminars/<int:pk>/', views.seminar_detail, name='seminar_detail'),
    path('seminars/question/<int:pk>/', views.seminar_question_detail, name='seminar_question_detail'),
    path('seminars/table/<int:pk>/', views.seminar_table_detail, name='seminar_table_detail'),
    path('statistics/', views.statistics, name='statistics'),
    path('my-results/', views.my_statistics, name='my_statistics'),
]
