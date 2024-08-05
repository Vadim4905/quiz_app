import random
from django.db import models
from django.core.exceptions import ValidationError

class UniqueRandomCode(models.IntegerField):
    def __init__(self, min_value=100_000, max_value=999_999, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(*args, **kwargs)

    def generate_unique_value(self, model_instance):
        model_class = model_instance.__class__
        while True:
            random_value = random.randint(self.min_value, self.max_value)
            if not model_class.objects.filter(**{self.name: random_value}).exists():
                return random_value

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is None:  # If the value is None, generate a unique value
            value = self.generate_unique_value(model_instance)
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)