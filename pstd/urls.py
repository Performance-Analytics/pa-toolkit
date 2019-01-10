from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('training-cycles/',
         views.training_cycle_list,
         name="list"),
    
    path('training-cycles/<int:training_cycle_id>/delete/',
         views.training_cycle_delete,
         name="delete"),

    path('training-cycles/new/',
         views.training_cycle_new,
         name="new"),

    path('training-cycles/<int:training_cycle_id>/edit/',
         views.training_cycle_edit,
         name="edit"),

    path('training-cycles/<int:training_cycle_id>/query/',
         views.session_query,
         name="query"),

    path('training-cycles/<int:training_cycle_id>/result/',
         views.session_result,
         name="result"),

]