from django.urls import path
from .views import AddGoalView, AllGoalsView


urlpatterns = [
    path('', AllGoalsView.as_view(), name='goals-list'),
    path('add/', AddGoalView.as_view(), name='goal-add'),

]
