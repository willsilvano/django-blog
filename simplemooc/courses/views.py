from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from simplemooc.courses.decorators import enrollment_required
from simplemooc.courses.forms import CommentForm
from simplemooc.courses.models import Enrollment, Lesson, Material
from .models import Course
from .forms import ContactCourse


def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['form'] = form
    context['course'] = course

    template_name = 'courses/details.html'
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, 'Você foi inscrito no curso com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito neste curso!')
    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
        return redirect('accounts:dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template_name = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    form = CommentForm(request.POST or None)
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template_name = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    template = 'courses/lessons.html'
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template, context)


@login_required
@enrollment_required
def show_lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, course=course, pk=pk)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=slug)
    template = 'courses/show_lesson.html'
    context = {
        'course': course,
        'lesson': lesson,
    }
    return render(request, template, context)


@login_required
@enrollment_required
def show_material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lessons', slug=slug)
    if not material.is_embedded():
        return redirect(material.file.url)
    template = 'courses/show_material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }
    return render(request, template, context)
