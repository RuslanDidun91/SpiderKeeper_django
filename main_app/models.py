from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
  ('1', '🦗'),
  ('2', '🐛'),
  ('3', '🪲')
)
# Create your models here.

class Decoration(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=100)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('decorations_detail', kwargs={'pk': self.id})

class Spider(models.Model):
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  level = models.CharField(max_length=50)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  #add M:M relationship
  decorations = models.ManyToManyField(Decoration)
  #add the FK linking to a user instance
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
  def __str__(self):
      return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'spider_id': self.id})

  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

class Feeding(models.Model):
  date = models.DateField('Feeding date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )
  #create spider_id Foreign Key
  #comes from another model
  spider = models.ForeignKey(
    Spider,
    #means we delete spider and all feedings from it
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"

#ordering list by recent date
  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  spider = models.ForeignKey(Spider, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for spider_id: {self.spider_id} @{self.url}"

