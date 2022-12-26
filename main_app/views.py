import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
#auth imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
###
from .models import Spider, Decoration, Photo
from .forms import FeedingForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def spiders_index(request):
    spiders = Spider.objects.filter(user=request.user)
    return render(request, 'spiders/index.html', {
        'spiders': spiders
    })

@login_required
def spiders_detail(request, spider_id):
    spider = Spider.objects.get(id=spider_id)
    # Get the decor the spider doesn't have..
    # First, create a list of the toy ids that the cat DOES have
    id_list = spider.decorations.all().values_list('id')
    # Now we can query for decor whose ids are not in the list using exclude
    decor_spider_doesnt_have = Decoration.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'spiders/detail.html', {
        'spider': spider,
        'feeding_form': feeding_form,
        'decorations': decor_spider_doesnt_have
    })

#authorization on clas-based views LoginRequiredMixin
class SpiderCreate(LoginRequiredMixin, CreateView):
    model = Spider
    fields = ['name', 'breed', 'description', 'age', 'level']

    def form_valid(self, form):
      # self.request.user is the logged in user
      form.instance.user = self.request.user
      # Let the CreateView's form_valid method
      # do its regular work (saving the object & redirecting)
      return super().form_valid(form)

class SpiderUpdate(LoginRequiredMixin, UpdateView):
    model = Spider
    fields = ['breed', 'description', 'age', 'level']

class SpiderDelete(LoginRequiredMixin, DeleteView):
    model = Spider
    success_url = '/spiders'

@login_required
def add_feeding(request, spider_id):
    # create a ModelForm instance using
    # the dta was submitted
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.spider_id = spider_id
        new_feeding.save()
    return redirect('detail', spider_id=spider_id)

class DecorationList(LoginRequiredMixin, ListView):
    model = Decoration

class DecorationDetail(LoginRequiredMixin, DetailView):
    model = Decoration

class DecorationCreate(LoginRequiredMixin, CreateView):
    model = Decoration
    fields = '__all__'

class DecorationUpdate(LoginRequiredMixin, UpdateView):
    model = Decoration
    fields = ['name', 'description']

class DecorationDelete(LoginRequiredMixin, DetailView):
    model = Decoration
    success_url = '/decorations'

@login_required
def assoc_decor(request, spider_id, decoration_id):
    Spider.objects.get(id=spider_id).decorations.add(decoration_id)
    return redirect('detail', spider_id=spider_id)

@login_required
def unassoc_decor(request, spider_id, decoration_id):
    Spider.objects.get(id=spider_id).decorations.remove(decoration_id)
    return redirect('detail', spider_id=spider_id)

@login_required
def add_photo(request, spider_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, spider_id=spider_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', spider_id=spider_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)