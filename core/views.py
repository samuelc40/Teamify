from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils.timezone import now
from django.db.models import Case, When, Value, IntegerField


from django.utils.timezone import now
from django.db.models import Q



@login_required(login_url='userauths:sign-in')
def index(request):

    current_user = request.user
    user_tasks = Task.objects.filter(assignee=current_user)
    team_tasks = Task.objects.filter(assignee_team__members=current_user)

    if current_user.is_superuser:
        all_tasks = Task.objects.all()
    else:
        all_tasks = user_tasks | team_tasks

    # Update tasks with past due dates to 'Pending'
    for task in all_tasks:
        if task.due_date < now().date():
            if task.category in ['New', 'Progress', 'Hold']:
                task.category = 'Pending'
                task.save()

    # Order tasks by custom priority: High (3), Medium (2), Low (1)
    all_tasks = all_tasks.annotate(
        priority_order=Case(
            When(priority='High', then=Value(3)),
            When(priority='Medium', then=Value(2)),
            When(priority='Low', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-priority_order', '-due_date')  # Orders by priority (High > Medium > Low)

    # Filtering tasks based on categories
    new_task = all_tasks.filter(category='New')
    progress_task = all_tasks.filter(category='Progress')
    hold_task = all_tasks.filter(category='Hold')
    pending_task = all_tasks.filter(category='Pending')

    for task in all_tasks:
        print(task.title)
    print("User object:", request.user)

    context = {
        'tasks': all_tasks,
        'new_task': new_task,
        'progress_task': progress_task,
        'hold_task': hold_task,
        'pending_task': pending_task,
    }

    return render(request, 'home.html', context)



# def task_view(request, task_id):
#     current_user = request.user
#     current_task = Task.objects.get(id=task_id)
#     error_text = ''
#     comment = None

#     if request.method == 'POST':
#         text = request.POST.get('comment')
#         if text == '':
#             print('Please enter any comment!')
#             error_text = 'Please enter something'
#         else:
#             comment = Comment.objects.create(
#                 user=current_user,
#                 text=text,
#                 task=current_task,
#             )
#             comment.save()  # Move the save() call here

#             return redirect('core:task', task_id=task_id)

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()

#     labels = Label.objects.all()
#     teams = Team.objects.all()
#     categories = Task.CATEGORY_CHOICES
#     all_users = User.objects.all()
#     users = User.objects.filter(is_staff=True)

#     context = {
#         'task': current_task, 
#         'user': current_user,
#         'comments': comments,
#         'error_text': error_text,
#         'labels': labels,
#         'teams': teams,
#         'categories': categories,
#         'all_users': all_users,
#         'users': users,
        
#     }

#     return render(request, 'task.html', context)


def create_task(request):
    labels = Label.objects.all()
    teams = Team.objects.all()
    categories = Task.CATEGORY_CHOICES
    all_users = User.objects.all()
    users = User.objects.filter(is_staff=True)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        get_labels = request.POST.getlist('labels')
        get_category = request.POST.get('category')
        assignee_id = request.POST.get('assignee_id')
        assignee_team_id = request.POST.get('assignee_team_id')
        created_by_id = request.POST.get('created_by_id')

        # Validate the data if necessary

        # Create the task object
        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=get_category,
            created_by_id=created_by_id
        )

        # Assign assignee if provided
        if assignee_id:
            task.assignee_id = assignee_id

        # Assign assignee team if provided
        if assignee_team_id:
            task.assignee_team_id = assignee_team_id

        # Assign labels if provided
        if get_labels:
            task.labels.add(*get_labels)

        # Save the task
        task.save()

        # Redirect to a success page or any other appropriate action
        return redirect('core:index')



    context = {
        'labels': labels,
        'teams': teams,
        'categories': categories,
        'users': users,
        'all_users': all_users,
    }
    return render(request, 'create_task.html', context)












from django.db import IntegrityError
def task_view(request, task_id):
    current_user = request.user
    current_task = get_object_or_404(Task, pk=task_id)
    error_text = ''

    if request.method == 'POST':
        if 'edit_task' in request.POST:
            # Retrieve form data
            title = request.POST.get('title')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            priority = request.POST.get('priority')
            get_labels = request.POST.getlist('labels')
            get_category = request.POST.get('category')
            assignee_id = request.POST.get('assignee_id')
            assignee_team_id = request.POST.get('assignee_team_id')

            # Debugging: Print retrieved category
            print("Selected Category:", get_category)

            try:
                # Update task fields
                current_task.title = title
                current_task.description = description
                current_task.due_date = due_date
                current_task.priority = priority

                # Validate and update category
                valid_categories = [choice[0] for choice in Task.CATEGORY_CHOICES]
                if get_category in valid_categories:
                    current_task.category = get_category
                else:
                    print("Invalid category selected.")

                # Update labels
                if get_labels:
                    labels = Label.objects.filter(id__in=get_labels)
                    current_task.labels.set(labels)

                # Update assignees
                current_task.assignee_id = assignee_id if assignee_id else None
                current_task.assignee_team_id = assignee_team_id if assignee_team_id else None

                # Save task
                current_task.save()
                print("Task updated successfully!")

                return redirect('core:task', task_id=task_id)
            except Exception as e:
                error_text = f"Error updating task: {e}"
                print(error_text)

    # Fetch comments and other context data
    context = {
        'task': current_task,
        'user': current_user,
        'error_text': error_text,
        'labels': Label.objects.all(),
        'teams': Team.objects.all(),
        'categories': Task.CATEGORY_CHOICES,
        'all_users': User.objects.all(),
        'users': User.objects.filter(is_staff=True),
        'comments': current_task.comments.all(),
    }

    return render(request, 'task.html', context)


# def edit_task(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     labels = Label.objects.all()
#     teams = Team.objects.all()
#     categories = Task.CATEGORY_CHOICES
#     all_users = User.objects.all()
#     users = User.objects.filter(is_staff=True)

#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         due_date = request.POST.get('due_date')
#         priority = request.POST.get('priority')
#         get_labels = request.POST.getlist('labels')
#         get_category = request.POST.get('category')
#         assignee_id = request.POST.get('assignee_id')
#         assignee_team_id = request.POST.get('assignee_team_id')
#         created_by_id = request.POST.get('created_by_id')

#         # Update the task object
#         task.title = title
#         task.description = description
#         task.due_date = due_date
#         task.priority = priority
#         task.category = get_category
#         task.created_by_id = created_by_id

#         # Assign assignee if provided
#         if assignee_id:
#             task.assignee_id = assignee_id
#         else:
#             task.assignee = None

#         # Assign assignee team if provided
#         if assignee_team_id:
#             task.assignee_team_id = assignee_team_id
#         else:
#             task.assignee_team = None

#         # Clear existing labels and assign new ones if provided
#         task.labels.clear()
#         if get_labels:
#             task.labels.add(*get_labels)

#         # Save the task
#         task.save()

#         # Redirect to a success page or any other appropriate action
#         return redirect('core:index')

#     context = {
#         'task': task,
#         'labels': labels,
#         'teams': teams,
#         'categories': categories,
#         'users': users,
#         'all_users': all_users,
#     }
#     return redirect('core:task', context, task_id=task_id)

# def comment_task(request, task_id):

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()
#     return render(request, )
   

# def task_view(request, task_id):
#     current_user = request.user
#     current_task = Task.objects.get(id=task_id)

#     if request.method == 'POST':
#         text = request.POST.get('comment')

#         comment = Comment.objects.create(
#             user=current_user,
#             text=text,
#             task=current_task,
#             )
#         comment.save()

#         return redirect('core:task', task_id=task_id)

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()

#     context = {
#         'task': current_task, 
#         'user': current_user,
#         'comments': comments,
#     }

#     return render(request, 'task.html', context)
