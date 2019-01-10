from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

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

def training_cycle_delete(request, training_cycle_id):
    training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)
    training_cycle.config.delete()

    return HttpResponseRedirect(reverse('list'))

def training_cycle_edit(request, training_cycle_id):
    training_cycle_name = request.POST.get('training_cycle_name')
    if training_cycle_name is not None: # Form handling.
        training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)

        training_cycle.name = training_cycle_name

        config = training_cycle.config

        # Construct config model from POST data.
        config.reps_per_set_small = request.POST["reps_per_set_small"]
        config.reps_per_set_medium = request.POST["reps_per_set_medium"]
        config.reps_per_set_large = request.POST["reps_per_set_large"]

        config.inol_target_small = request.POST["inol_target_small"]
        config.inol_target_medium = request.POST["inol_target_medium"]
        config.inol_target_large = request.POST["inol_target_large"]

        config.intensity_target_small = request.POST["intensity_target_small"]
        config.intensity_target_medium = request.POST["intensity_target_medium"]
        config.intensity_target_large = request.POST["intensity_target_large"]

        config.supramaximal_inol_increment = request.POST["supramaximal_inol_increment"]

        # Save models into database.
        config.save()
        training_cycle.save()

        # Redirect.
        return HttpResponseRedirect('/pstd/training-cycles/')
    else: # Form rendering.
        training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)
        context = {
            'new_cycle': False,
            'training_cycle': training_cycle
        }
        return render(request, 'pstd/edit.html', context)

def training_cycle_new(request):
    training_cycle_name = request.POST.get('training_cycle_name')
    if training_cycle_name is not None: # Form handling.
        training_cycle = TrainingCycle()

        training_cycle.name = training_cycle_name

        config = TrainingCycleConfig()

        # Construct config model from POST data.
        config.reps_per_set_small = request.POST["reps_per_set_small"]
        config.reps_per_set_medium = request.POST["reps_per_set_medium"]
        config.reps_per_set_large = request.POST["reps_per_set_large"]

        config.inol_target_small = request.POST["inol_target_small"]
        config.inol_target_medium = request.POST["inol_target_medium"]
        config.inol_target_large = request.POST["inol_target_large"]

        config.intensity_target_small = request.POST["intensity_target_small"]
        config.intensity_target_medium = request.POST["intensity_target_medium"]
        config.intensity_target_large = request.POST["intensity_target_large"]

        config.supramaximal_inol_increment = request.POST["supramaximal_inol_increment"]

        # Save config model into database.
        config.save()

        # Build and save a training cycle from the config into database.
        training_cycle.config = config
        training_cycle.save()
        
        # Redirect.
        return HttpResponseRedirect('/pstd/training-cycles/')
    else: # Form rendering.
        context = {'new_cycle': True}
        return render(request, 'pstd/edit.html', context)

def training_cycle_list(request):
    training_cycles = TrainingCycle.objects.all()
    context = {'training_cycles': training_cycles}
    return render(request, 'pstd/list.html', context)
