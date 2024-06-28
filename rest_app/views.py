from django.shortcuts import render,redirect
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework .permissions import AllowAny
from django .http import HttpResponse
from .forms import TouristplacesForm
import requests
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,InvalidPage
class TourCreateView(generics.ListCreateAPIView):
    queryset = Touristplaces.objects.all()
    serializer_class =Tourserializers
    permission_classes = [AllowAny]
class TourDetail(generics.RetrieveAPIView):
    queryset = Touristplaces.objects.all()
    serializer_class = Tourserializers
class TourUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Touristplaces.objects.all()
    serializer_class = Tourserializers
class TourDelete(generics.DestroyAPIView):
    queryset = Touristplaces.objects.all()
    serializer_class =Tourserializers
class TourSearchViewSet(generics.ListAPIView):
    queryset = Touristplaces.objects.all()
    serializer_class = Tourserializers

    def get_queryset(self):
        name = self.kwargs.get('Name')
        return Touristplaces.objects.filter(Name__icontains=name)
def index(request):
    return render(request,'base.html')
def create_tour(request):
    if request.method == 'POST':
        form = TouristplacesForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url='http://127.0.0.1:8000/create/'
                data=form.cleaned_data
                print(data)

                response=request.post(api_url, data=data ,files={'Tour_img':request.FILES['Tour_img']})

                if response.status_code == 400:
                    messages.success(request, 'Tour inserted successfully')

                else:
                    messages.error(request, f'Error{response.status_code}')
            except requests.RequestException as e:
                messages.error(request,f'Error during API request {str(e)}')
        else:
            messages.error(request,'Form is not valid')
    else:
        form=TouristplacesForm()
    return render(request,'create_tour.html',{'form':form})

def update_detail(request,id):
    api_url=f'http://127.0.0.1:8000/detail/{id}/'
    response=requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
    return render(request, 'tour_update.html',{'tour':data})

def update_tour(request,id):
    if request.method == 'POST':
        name = request.POST['Name']
        weather = request.POST['Weather']
        location_state = request.POST['Location_State']
        location_district = request.POST['Location_District']
        print('Image Url', request.FILES.get('Tour_img'))
        description = request.POST['Description']

        api_url = f'http://127.0.0.1:8000/update/{id}/'

        data = {
            'Name' : name,
            'Weather' : weather,
            'Location State' : location_state,
            'Location District' : location_district,
            'Description' : description
        }
    files = {'Tour_image' : request.FILES.get('Tour_image')}

    response = request.put(api_url, data=data ,files=files)
    if response.status_code == 200:
        messages.success(request, 'Tour updated successfully')
        return redirect('/')
    else:
        messages.error(request, f'Error submitting data to the REST API : {response.status_code}')
    return render(request, 'tour_update.html')

def index(request):
    if request.method == 'POST':
        search = request.POST['Search']

        api_url = f'http://127.0.0.1:8000/search/{search}'

        try:
            response = requests.get(api_url)

            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
            else:
                data=None
        except requests.RequestException as e:
            data=None

        return render(request, 'index.html',{'data' :data})
    else:
        api_url = f'http://127.0.0.1:8000/create/'
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                original_data=data

                paginator=Paginator(original_data, 6)

                try:
                    page=int(request.GET.get('page',1))
                except:
                    page = 1
                try:
                    tour=paginator.page(page)
                except(EmptyPage,InvalidPage):
                    tour = Paginator.page(paginator.num_pages)

                context = {
                    'original_data':original_data,
                    'tour':tour
                }
                return render(request,'index.html',context)
            else:
                return render(request,'index.html',{'error_message':f'Error:{response.status_code}'})
        except requests.RequestException as e:
            return render(request,'index.html',{'error message':f'Error:{str(e)}'})
    return render(request,'index.html')


def tour_fetch(request,id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return render(request, 'tour_fetch.html', {'tour': data})
    return render(request,'tour_fetch.html')

def tour_delete(request,id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'

    response = requests.delete(api_url)

    if response.status_code == 200:
        print(f'Item with id{id} has been deleted')
    else:
        print(f'Failed to delete item,status code {response.status_code}')
    return redirect('/')
