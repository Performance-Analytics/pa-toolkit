from django.db import models
from django.contrib.auth.models import User

class TrainingCycleConfig(models.Model):
    reps_per_set_small = models.PositiveSmallIntegerField()
    reps_per_set_medium = models.PositiveSmallIntegerField()
    reps_per_set_large = models.PositiveSmallIntegerField()

    inol_target_small = models.FloatField()
    inol_target_medium = models.FloatField()
    inol_target_large = models.FloatField()

    intensity_target_small = models.FloatField()
    intensity_target_medium = models.FloatField()
    intensity_target_large = models.FloatField()

    supramaximal_inol_increment = models.FloatField()


class TrainingCycle(models.Model):
    config = models.ForeignKey(TrainingCycleConfig, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_training_max = models.FloatField(default=0)
    name = models.CharField(max_length=256, default="default")
