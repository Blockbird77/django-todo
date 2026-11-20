from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

# Create your views here.
def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', 'Medium')
        if title:
            Task.objects.create(title=title, priority=priority)
        return redirect('task_list')

    tasks = Task.objects.all().order_by('completed', '-created_at')
    pending_count = Task.objects.filter(completed=False).count()
    completed_count = Task.objects.filter(completed=True).count()

    context = {
        'tasks': tasks,
        'pending_count': pending_count,
        'completed_count': completed_count,
    }
    return render(request, 'todo/task_list.html', context)

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', 'Medium')
        if title:
            task.title = title
            task.priority = priority
            task.save() 
        return redirect('task_list')

    return render(request, 'todo/edit_task.html', {'task': task})

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')