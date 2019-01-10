from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models.training_cycles import TrainingCycle, TrainingCycleConfig

from .models.training_sessions import SessionGenerator

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at PSTD index.")

def session(request, training_cycle_id):
    training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)
    context = {'training_cycle': training_cycle}
    if request.method == "POST":
        context['session'] = SessionGenerator(
            training_cycle,
            request.POST['fatigue_rating'],
            float(request.POST['training_max'])
        ).session

    return render(request, 'pstd/session.html', context)

def training_cycle_delete(request, training_cycle_id):
    training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)
    training_cycle.config.delete()

    return HttpResponseRedirect(reverse('list'))

def training_cycle_edit(request, training_cycle_id):
    training_cycle_name = request.POST.get('training_cycle_name')
    if request.method == "POST":
        training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)

        training_cycle.name = training_cycle_name
        training_cycle.user = request.user

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
        return HttpResponseRedirect(reverse('list'))
    else:
        training_cycle = TrainingCycle.objects.get(pk=training_cycle_id)
        context = {'training_cycle': training_cycle}
        return render(request, 'pstd/edit.html', context)

def training_cycle_new(request):
    training_cycle_name = request.POST.get('training_cycle_name')
    if request.method == "POST":
        training_cycle = TrainingCycle()

        training_cycle.name = training_cycle_name
        training_cycle.user = request.user

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
        return HttpResponseRedirect(reverse('list'))
    else:
        return render(request, 'pstd/edit.html')

def training_cycle_list(request):
    training_cycles = TrainingCycle.objects.filter(user=request.user.pk)
    context = {'training_cycles': training_cycles}
    return render(request, 'pstd/list.html', context)
