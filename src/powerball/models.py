import django
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


def get_user_model_fk_ref():
    if django.VERSION[:2] >= (1, 5):
        return settings.AUTH_USER_MODEL
    else:
        return 'auth.User'

class Drawentry(models.Model):
    user = models.OneToOneField(get_user_model_fk_ref())
    user.primary_key = True
    balls = ArrayField(models.PositiveIntegerField(validators=[
        MaxValueValidator(69), MinValueValidator(1)] ),
                       blank=False,
                       size=5)
    powerball = models.PositiveIntegerField(blank=False, validators=[
        MaxValueValidator(26), MinValueValidator(1),])

    def __str__(self):
        return self.balls