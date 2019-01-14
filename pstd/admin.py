from django.contrib import admin

from .models.training_cycles import PresetTrainingCycle, TrainingCycle, TrainingCycleConfig

# Register your models here.

admin.site.register(PresetTrainingCycle)
admin.site.register(TrainingCycle)
admin.site.register(TrainingCycleConfig)
