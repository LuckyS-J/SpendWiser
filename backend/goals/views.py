from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import GoalForm, ProgressForm
from .models import Goal
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AllGoalsView(LoginRequiredMixin, View):
    def get(self, request):
        
        goals = Goal.objects.filter(user=request.user)
        goals.order_by('-created_at')
        completed_count = sum(1 for g in goals if g.is_completed)
        in_progress_count = sum(1 for g in goals if not g.is_completed)

        return render(request, 'goals/goals_list.html', {
          'goals':goals,
          'completed_count': completed_count,
          'in_progress_count': in_progress_count,
         }
        )

class AddGoalView(LoginRequiredMixin, View):
    def get(self, request):

        form = GoalForm()
        return render(request, 'goals/add_goal.html', {'form': form})

    def post(self, request):

        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals-list')
        return render(request, 'goals/add_goal.html', {'form': form})

class DeleteGoalView(LoginRequiredMixin, View):
    def post(self, request, id):
        goal = get_object_or_404(Goal, user=request.user, id=id)
        goal.delete()
        return redirect('goals-list')
    
class AddProgressView(LoginRequiredMixin, View):
    def get(self, request, id):
        goal = get_object_or_404(Goal, user=request.user, id=id)
        form = ProgressForm(goal=goal)
        return render(request, 'goals/add_progress.html', {'form':form})
    
    def post(self, request, id):
        goal = get_object_or_404(Goal, user=request.user, id=id)
        form = ProgressForm(request.POST, goal=goal)
        if form.is_valid():
            progress = form.cleaned_data['progress']
            goal.current += progress
            goal.save()
            return redirect('goals-list')
        return render(request, 'goals/add_progress.html', {'form': form})
