# views for handling modules, enrollment, roles and uploads
# each view matches one feature or page in the app


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Module, User, TrainerAssignment, Enrollment
from django.contrib import messages
from collections import defaultdict
from .models import Module, ModuleFile
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect


# add a new module
def add_module(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Module.objects.create(title=title, description=description)
        return redirect('/admin-dashboard/')  # go back to admin dashboard

    return render(request, 'add_module.html')


# update a module
def edit_module(request, module_id):
    module = Module.objects.get(id=module_id)

    if request.method == 'POST':
        module.title = request.POST.get('title')
        module.description = request.POST.get('description')
        module.save()
        return redirect('/admin-dashboard/')  # going back to admin page after editing

    return render(request, 'edit_module.html', {'module': module})


# remove a module
def delete_module(request, module_id):
    module = Module.objects.get(id=module_id)

    if request.method == 'POST':
        module.delete()
        return redirect('/admin-dashboard/')

    return render(request, 'delete_module.html', {'module': module})


# link trainer to a module
def assign_trainer(request):
    trainers = User.objects.filter(role='trainer')
    modules = Module.objects.all()

    if request.method == 'POST':
        trainer_id = request.POST.get('trainer')
        module_id = request.POST.get('module')
        trainer = User.objects.get(id=trainer_id)
        module = Module.objects.get(id=module_id)
        TrainerAssignment.objects.create(user=trainer, module=module)

        messages.success(request, f"{trainer.username} was assigned to {module.title} successfully.")  # confirmation message
        return redirect('/admin-dashboard/')

    return render(request, 'assign_trainer.html', {'trainers': trainers, 'modules': modules})


# show trainer's assigned modules
def trainer_modules(request):
    trainer = request.user  # dynamic login
    assignments = TrainerAssignment.objects.filter(user=trainer).select_related('module')
    return render(request, 'trainer_modules.html', {'assignments': assignments})


# enroll student to module (trainer role)
def enroll_student(request):
    trainer = request.user
    assignments = TrainerAssignment.objects.filter(user=trainer)
    modules = [a.module for a in assignments]
    students = User.objects.filter(role='student')

    if request.method == 'POST':
        student_id = request.POST.get('student')
        module_id = request.POST.get('module')

        student = User.objects.get(id=student_id)
        module = Module.objects.get(id=module_id)

        Enrollment.objects.create(user=student, module=module)
        messages.success(request, "Student enrolled successfully.")


    return render(request, 'enroll_student.html', {
        'modules': modules,
        'students': students
    })


# remove student from module
def remove_student(request):
    trainer = User.objects.get(username='trainer1')
    assignments = TrainerAssignment.objects.filter(user=trainer)
    modules = [a.module for a in assignments]

    selected_module = None
    enrollments = []

    if request.method == 'POST':
        module_id = request.POST.get('module')
        student_id = request.POST.get('student')

        if module_id and student_id:
            student = User.objects.get(id=student_id)
            module = Module.objects.get(id=module_id)
            Enrollment.objects.filter(user=student, module=module).delete()
            messages.success(request, "Student removed successfully.")
            return redirect('remove_student')

        elif module_id:
            selected_module = Module.objects.get(id=module_id)
            enrollments = Enrollment.objects.filter(module=selected_module)

    return render(request, 'remove_student.html', {
        'modules': modules,
        'enrollments': enrollments,
        'selected_module': selected_module
    })


# save module notes (trainer only)
def update_notes(request, module_id):
    trainer = User.objects.get(username='trainer1')
    module = Module.objects.get(id=module_id)

    if not TrainerAssignment.objects.filter(user=trainer, module=module).exists():
        return redirect('/trainer-modules/')

    if request.method == 'POST':
        notes = request.POST.get('notes')
        module.notes = notes
        module.save()
        messages.success(request, "Notes updated successfully.")

    return render(request, 'update_notes.html', {'module': module})


# list student's enrolled modules
def student_modules(request):
    student = request.user
    enrollments = Enrollment.objects.filter(user=student)
    return render(request, 'student_modules.html', {'enrollments': enrollments})


# student self-enroll to new module
def self_enroll(request):
    if request.method == 'POST':
        module_id = request.POST.get('module_id')

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return redirect('/browse-modules/')  

        Enrollment.objects.create(user=request.user, module=module)
        return redirect('/student-modules/')


# list modules student is not enrolled in
def browse_modules(request):
    student = request.user
    enrolled = Enrollment.objects.filter(user=student).values_list('module', flat=True)
    modules = Module.objects.exclude(id__in=enrolled)
    return render(request, 'browse_modules.html', {'modules': modules})


# student reads module content
def view_module_content(request, module_id):
    user = User.objects.get(username='student1')  # temporary
    try:
        enrollment = Enrollment.objects.get(user=user, module__id=module_id)
        module = enrollment.module
    except Enrollment.DoesNotExist:
        return redirect('/student-modules/')

    return render(request, 'view_module.html', {'module': module})


# trainer sees full module content
def trainer_module_detail(request, module_id):
    if request.user.role != 'trainer':
        return redirect('/login/')

    module = Module.objects.get(id=module_id)

    # fetch all files for the module
    files = ModuleFile.objects.filter(module=module)

    # group by week 
    weeks = []
    for week_num in range(1, 11):
        week_files = files.filter(week=week_num)
        weeks.append({
            'week': week_num,
            'files': week_files
        })

    return render(request, 'trainer_view_module.html', {
        'module': module,
        'weeks': weeks
    })


# student sees weekly uploads
def student_module_detail(request, module_id):
    if request.user.role != 'student':
        return redirect('/login/')

    module = Module.objects.get(id=module_id)
    files = ModuleFile.objects.filter(module=module)

    weeks = []
    for week_num in range(1, 11):
        week_files = files.filter(week=week_num)
        weeks.append({
            'week': week_num,
            'files': week_files
        })

    return render(request, 'student_view_module.html', {
        'module': module,
        'weeks': weeks
    })


# send user to their dashboard
def role_redirect(request):
    if request.user.role == 'admin':
        return redirect('/admin-dashboard/')  
    elif request.user.role == 'trainer':
        return redirect('/trainer-modules/')
    elif request.user.role == 'student':
        return redirect('/student-modules/')
    else:
        return redirect('/login/')


# show admin dashboard with modules and trainers
def admin_dashboard(request):
    modules = Module.objects.all()
    assignments = TrainerAssignment.objects.select_related('user', 'module')

    # collect trainers for each module.id
    module_trainers = defaultdict(list)
    for assignment in assignments:
        module_trainers[assignment.module.id].append(assignment.user.username)

    # convert keys to string for use in template
    joined_trainers = {str(k): ", ".join(v) for k, v in module_trainers.items()}

    return render(request, 'admin_dashboard.html', {
        'modules': modules,
        'module_trainers': joined_trainers
    })


# remove uploaded file
def delete_file(request, file_id):
    file = get_object_or_404(ModuleFile, id=file_id)
    module_id = file.module.id
    file.delete()
    return redirect('trainer_module_detail', module_id=module_id)


# upload file for module week
def upload_file(request, module_id, week):
    if request.method == 'POST' and request.user.role == 'trainer':
        module = Module.objects.get(id=module_id)
        uploaded_file = request.FILES['file']
        title = request.POST.get('title', '')

        ModuleFile.objects.create(
            module=module,
            week=week,
            title=title,
            file=uploaded_file
        )

    return redirect('trainer_module_detail', module_id=module_id)


# logout and redirect to login
def custom_logout(request):
    logout(request)
    return redirect('/login/')


# home page
def index(request):
    return render(request, 'index.html')


