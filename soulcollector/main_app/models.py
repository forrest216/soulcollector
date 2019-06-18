from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

MEALS = (
   ('B', 'Brimstone'),
   ('F', 'Fire'),
   ('T', 'Tacos'),
   ('C', 'Cotton Candy'),
)

class Instrument(models.Model):
   name = models.CharField(max_length=50)
   material = models.CharField(max_length=20)
   def __str__(self):
      return self.name
   def get_absolute_url(self):
      return reverse('instruments_detail', kwargs={'pk': self.id})

class Soul(models.Model):
   name = models.CharField(max_length=100)
   cause = models.CharField(max_length=100)
   notes = models.CharField(max_length=250)
   age = models.IntegerField()
   instruments = models.ManyToManyField(Instrument)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   def __str__(self):
      return self.name
   def get_absolute_url(self):
      return reverse('show', kwargs={'soul_id': self.id})
   def fed_today(self):
      return self.meal_set.filter(date=date.today()).count() >= len(MEALS)/2

class Meal(models.Model):
   date = models.DateField('meal date')
   meal = models.CharField(
      max_length=1,
      choices=MEALS,
      default=MEALS[0][0]
   )
   soul = models.ForeignKey(Soul, on_delete=models.CASCADE)
   def __str__(self):
      return f"{self.get_meal_display()} on {self.date}"
   class Meta:
      ordering = ['-date']

class Photo(models.Model):
   url = models.CharField(max_length=200)
   soul = models.ForeignKey(Soul, on_delete=models.CASCADE)
   def __str__(self):
      return f"Photo for soul_id: {self.soul_id} @{self.url}"