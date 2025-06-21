from django.shortcuts import render, redirect
from django.views import View
from .forms import GoalForm
from .models import Goal

# Create your views here.


class AllGoalsView(View):
    def get(self, request):
        
        goals = Goal.objects.filter(user=request.user)
        goals.order_by('-created_at')
        completed_count = [g for g in goals if g.is_completed]
        in_progress_count = [g for g in goals if not g.is_completed]

        return render(request, 'goals/goals_list.html', {
          'goals':goals,
          'completed_count': completed_count,
          'in_progress_count': in_progress_count,
         }
        )

class AddGoalView(View):
    def get(self, request):

        form = GoalForm()
        return render(request, 'goals/add_goal.html', {'form': form})

    def post(self, request):

        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('home-page')
        return render(request, 'goals/add_goal.html', {'form': form})
