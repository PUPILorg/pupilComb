from django.db import models

from pupilComb.settings import AUTH_USER_MODEL

class Professor(models.Model):

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)