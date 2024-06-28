from django .urls import path
from .views import *
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('create/',TourCreateView.as_view(),name="Create Tour Place"),
    path('detail/<int:pk>/',TourDetail.as_view(),name="Detail"),
    path('update/<int:pk>/',TourUpdateView.as_view(),name="Update Tour Place"),
    path('delete/<int:pk>/',TourDelete.as_view(),name="Delete Tour Place"),
    path('search/<str:Name>/',TourSearchViewSet.as_view(),name="Search"),

    path('create_tour/',views.create_tour,name='create_tour'),
    path('tour_fetch/<int:pd>/',views.tour_fetch,name='tour_fetch'),
    path('update_tour/<int:pd>/',views.update_tour,name='update_tour'),
    path('tour_delete/<int:pd>/',views.tour_delete,name='tour_delete'),
    path('update_detail/<int:pd>/',views.update_detail,name='update_detail'),

]