from django.db import models

# should use the special method to find the user
from django.contrib.auth import get_user_model
# we don't want to do a direct import - use `get_user_model` instead
# from .user import User
# Create your models here.
class Mango(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  ripe = models.BooleanField()
  color = models.CharField(max_length=100)
  # For user ownership - a new field `owner` which keeps track
  # of the ID of the user that owns this Mango
  owner = models.ForeignKey(
      # lazy way
      # 'User'
      # import the model
      # User
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The mango named '{self.name}' is {self.color} in color. It is {self.ripe} that it is ripe."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name,
        'ripe': self.ripe,
        'color': self.color
    }
