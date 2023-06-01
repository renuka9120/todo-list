from django.shortcuts import render, get_object_or_404, redirect
from .models import Task,Tag


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'OPEN')
        tags_input = request.POST.get('tags', '')
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        task = Task.objects.create(title=title, description=description, due_date=due_date, status=status)
        for tag in tags:
            try:
                tag_obj, _ = Tag.objects.get_or_create(value=tag)
                task.tags.add(tag_obj)
            except ValueError:
                # Skip invalid tags
                continue

        return redirect('task_detail', pk=task.pk)

    return render(request, 'task_create.html')




def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'OPEN')
        tags_input = request.POST.get('tags', '')
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status
        task.tags.clear()  # Clear existing tags

        for tag in tags:
            try:
                tag_obj, _ = Tag.objects.get_or_create(value=tag)
                task.tags.add(tag_obj)
            except ValueError:
                # Skip invalid tags
                continue

        task.save()
        return redirect('task_detail', pk=task.pk)

    return render(request, 'task_update.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'task_delete.html', {'task': task})
