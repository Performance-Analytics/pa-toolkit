from django.urls import path

from . import views

urlpatterns = [

    path('', views.training_cycle_list, name='index'),

    path('training-cycles/',
         views.training_cycle_list,
         name="list"),
    
    path('training-cycles/<int:training_cycle_id>/delete/',
         views.training_cycle_delete,
         name="delete"),

    path('training-cycles/<int:training_cycle_id>/duplicate/',
         views.training_cycle_duplicate,
         name="duplicate"),

    path('training-cycles/new/',
         views.training_cycle_new,
         name="new"),

    path('training-cycles/<int:training_cycle_id>/edit/',
         views.training_cycle_edit,
         name="edit"),

    path('training-cycles/<int:training_cycle_id>/session/',
         views.session,
         name="session"),

]