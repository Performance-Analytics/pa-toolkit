from django.contrib import admin

from .models.training_cycles import TrainingCycle, TrainingCycleConfig

# Register your models here.

admin.site.register(TrainingCycle)
admin.site.register(TrainingCycleConfig)
