from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import TrainingCycle, TrainingCycleConfig

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at PSTD index.")

def session_query(request, training_cycle_id):
    return HttpResponse("Querying for a session in training cycle {}.".format(
        training_cycle_id
    ))

def session_result(request, training_cycle_id):
    return HttpResponse("Displaying a session in training cycle {}.".format(
        training_cycle_id
    ))

def training_cycle_edit(request, training_cycle_id):
    return HttpResponse("Editing training cycle {}.".format(training_cycle_id))

def training_cycle_list(request):
    training_cycles = TrainingCycle.objects.all()
    
    template = loader.get_template('pstd/list.html')
    context = {
        'training_cycles': training_cycles
    }
    return HttpResponse(template.render(context, request))