from django.urls import path
from .views import (
    DiscussionMainView,
    DiscussionCreateView,
    DiscussionDetailView
)
 
urlpatterns = [
    path('', DiscussionMainView.as_view(), name='discussion_main'),
    path('<int:pk>/', DiscussionDetailView.as_view(), name='discussion_detail'),
    path('create/', DiscussionCreateView.as_view(), name='discussion_form')
]
