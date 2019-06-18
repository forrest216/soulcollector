from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MealForm
import uuid
import boto3
from .models import Soul, Instrument, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'soulcollector'

@login_required
def index(request):
   souls = Soul.objects.filter(user=request.user)
   return render(request, 'index.html', {'souls': souls})

@login_required
def show(request, soul_id):
   soul = Soul.objects.get(id=soul_id)
   instruments_soul_doesnt_have = Instrument.objects.exclude(id__in=soul.instruments.all().values_list('id'))
   meal_form = MealForm()
   return render(request, 'show.html', {
      'soul': soul, 
      'meal_form': meal_form,
      'instruments': instruments_soul_doesnt_have
      })

@login_required
def add_meal(request, soul_id):
   form = MealForm(request.POST)
   if form.is_valid():
      new_meal = form.save(commit=False)
      new_meal.soul_id = soul_id
      new_meal.save()
   return redirect('show', soul_id=soul_id)

@login_required
def add_photo(request, soul_id):
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
         s3.upload_fileobj(photo_file, BUCKET, key)
         # build the full url string
         url = f"{S3_BASE_URL}{BUCKET}/{key}"
         # we can assign to soul_id or soul (if you have a soul object)
         photo = Photo(url=url, soul_id=soul_id)
         photo.save()
      except:
         print('An error occurred uploading file to S3')
   return redirect('show', soul_id=soul_id)

@login_required
def assoc_instrument(request, soul_id, instrument_id):
   Soul.objects.get(id=soul_id).instruments.add(instrument_id)
   return redirect('show', soul_id=soul_id)

@login_required
def unassoc_instrument(request, soul_id, instrument_id):
   Soul.objects.get(id=soul_id).instruments.remove(instrument_id)
   return redirect('show', soul_id=soul_id)

def about(request):
   return render(request, 'about.html')

def signup(request):
   error_message = ''
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save()
         login(request, user)
         return redirect('index')
      else:
         error_message = 'Invalid sign up - try again'
   form = UserCreationForm()
   context = {'form': form, 'error_message': error_message}
   return render(request, 'registration/signup.html', context)

class SoulCreate(LoginRequiredMixin, CreateView):
   model = Soul
   fields = ['name', 'age', 'cause', 'notes']
   success_url = '/'
   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class SoulUpdate(LoginRequiredMixin, UpdateView):
   model = Soul
   fields = ['age', 'cause', 'notes']

class SoulDelete(LoginRequiredMixin, DeleteView):
   model = Soul
   success_url = '/'

class InstrumentList(LoginRequiredMixin, ListView):
   model = Instrument

class InstrumentDetail(LoginRequiredMixin, DetailView):
   model = Instrument

class InstrumentCreate(LoginRequiredMixin, CreateView):
   model = Instrument
   fields = '__all__'

class InstrumentUpdate(LoginRequiredMixin, UpdateView):
   model = Instrument
   fields = ['name', 'material']

class InstrumentDelete(LoginRequiredMixin, DeleteView):
   model = Instrument
   success_url = '/instruments/'

