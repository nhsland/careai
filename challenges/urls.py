from django.urls import include, path
from . import views
from .views import (
    ChallengeMainView,
    ChallengeCreateView,
    ChallengeUpdateView,
    ChallengeDeleteView,
    ChallengeOverviewView,
    ChallengeDataView,
    ChallengeRulesView,
    ChallengeSolutionsView
)

urlpatterns = [
    path('', ChallengeMainView.as_view(), name='challenges_main'),
    path('<int:pk>/', ChallengeOverviewView.as_view(), name='challenges_detail'),
    path('create/', ChallengeCreateView.as_view(), name='challenges_create'),
    path('<challengeid>/participate', views.participate_in_challenge, name='participate'),
    path('<challengeid>/leavechallenge', views.leave_challenge, name='leave'),
    path('<int:pk>/update', ChallengeUpdateView.as_view(), name='challenges_update'),
    path('<int:pk>/delete', ChallengeDeleteView.as_view(), name='challenges_delete'),
    path('<int:pk>/overview', ChallengeOverviewView.as_view(), name='challenges_overview'),
    path('<int:pk>/data', ChallengeDataView.as_view(), name='challenges_data'),
    path('<int:pk>/solutions', ChallengeSolutionsView.as_view(), name='challenges_solutions'),
    path('<int:pk>/rules', ChallengeRulesView.as_view(), name='challenges_rules')

]
