from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url, include
from .views import (
    SolutionCreateView,
    SolutionDetailView,
    SolutionDeleteView,
    SolutionMainView,
    SolutionUpdateView,
    SolutionEvaluateView
)
 
urlpatterns = [
    path('', SolutionMainView.as_view(), name='solutions_main'),
    path('<int:pk>/', SolutionDetailView.as_view(), name='solutions_detail'),
    path('create/<challengepk>', SolutionCreateView.as_view(), name = 'solutions_create'),
    path('<int:pk>/update', SolutionUpdateView.as_view(), name = 'solutions_update'),
    path('<int:pk>/evaluate', SolutionEvaluateView.as_view(), name = 'solutions_evaluate'),
    path('<int:pk>/delete', SolutionDeleteView.as_view(), name = 'solutions_delete')
]