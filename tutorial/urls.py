from django.urls import path
from .views import (
    TutorialCreateView,
    TutorialMainView,
    TutorialOverviewView,
    TutorialDataView,
    TutorialUpdateView,
    TutorialDeleteView
)

urlpatterns = [
    path('', TutorialMainView.as_view(), name='tutorial_main'),
    path('create/', TutorialCreateView.as_view(), name='tutorial_create'),
    path('<int:pk>/', TutorialOverviewView.as_view(), name='tutorial_detail'),
    path('<int:pk>/overview', TutorialOverviewView.as_view(), name='tutorial_overview'),
    path('<int:pk>/data', TutorialDataView.as_view(), name='tutorial_data'),
    path('<int:pk>/update', TutorialUpdateView.as_view(), name='tutorial_update'),
    path('<int:pk>/delete', TutorialDeleteView.as_view(), name='tutorial_delete'),
]