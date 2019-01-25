class SessionGenerator(object):

    session: "TrainingSession"

    def __init__(self,
                 training_cycle,
                 fatigue_rating,
                 current_training_max):
        load_size = self.determine_load_size(
            fatigue_rating,
            training_cycle.previous_large_load_training_max,
            current_training_max
        )
        self.session = self.generate_session(training_cycle.config,
                                        load_size,
                                        current_training_max)

        training_cycle.previous_training_max = current_training_max
        if fatigue_rating == "low":
            training_cycle.previous_large_load_training_max = current_training_max
        training_cycle.save()

    def determine_load_size(self,
                            fatigue_rating,
                            previous_large_load_training_max,
                            current_training_max):
        if current_training_max > previous_large_load_training_max: # TM improved from last fresh session.
                return {
                    'low': 'large',
                    'medium': 'medium',
                    'high': 'medium'
                }[fatigue_rating]
        else: # TM stagnated or regressed from last fresh session.
            return {
                'low': 'supramaximal',
                'medium': 'medium',
                'high': 'small'
            }[fatigue_rating]
    
    def generate_session(self, config, load_size, training_max):
        def calculate_set_quantity(reps_per_set, intensity, inol):
            '''
            Calculates the sets required to accomplish the work desired.

            `extra_reps` is how many repetitions are left over after the
            calculated number of flat (specified repetition quantity) sets. For
            instance, if the user needs to complete 18 repetitions in sets of
            5, `extra_reps` will be 3.

            Returns a tuple comprising `(sets, extra_reps)`.
            '''
            total_reps = round(inol * 100 * (1 - intensity))

            extra_reps = round(total_reps % reps_per_set)
            sets = round((total_reps - extra_reps) / reps_per_set)
            return sets, extra_reps
        
        if load_size == 'supramaximal':
            config.inol_target_large += config.supramaximal_inol_increment
            config.save()
            load_size = 'large'
        
        load_size_map = {
            'reps_per_set': {
                'small': config.reps_per_set_small,
                'medium': config.reps_per_set_medium,
                'large': config.reps_per_set_large
            },
            'inol_targets': {
                'small': config.inol_target_small,
                'medium': config.inol_target_medium,
                'large': config.inol_target_large
            },
            'intensity_targets': {
                'small': config.intensity_target_small,
                'medium': config.intensity_target_medium,
                'large': config.intensity_target_large
            }
        }

        sets, extra_reps = calculate_set_quantity(
            load_size_map['reps_per_set'][load_size],
            load_size_map['intensity_targets'][load_size],
            load_size_map['inol_targets'][load_size]
        )

        session = TrainingSession(
            sets=sets,
            reps_per_set=load_size_map['reps_per_set'][load_size],
            extra_reps=extra_reps,
            intensity=load_size_map['intensity_targets'][load_size],
            training_max=training_max
        )

        return session

class TrainingSession(object):

    sets: int
    reps_per_set: int
    extra_reps: int
    intensity: float
    training_max: float

    def __init__(self, **kwargs):
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])
    
    @property
    def e1rm(self):
        return self.training_max / 0.9
    
    @property
    def load(self):
        return self.intensity * self.e1rm
