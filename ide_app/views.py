from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from subprocess import Popen, PIPE
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ide_app.models import Project, File
import sys
import subprocess

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def index(request):
    return render(request, "index.html")

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Username or email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)

        return redirect('home')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile_page')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    projects = Project.objects.filter(owner=request.user)
    context = {
        'user': request.user,
        'projects': projects
    }
    return render(request,'profile.html', context)

def code_ide(request):
    code = ""
    output = ""
    error = ""
    user_input = ""

    if request.method == 'POST':
        code = request.POST.get('code')
        user_input = request.POST.get('user_input')  # Retrieve user input

        try:
            # Execute the code using subprocess (include user input if any)
            process = subprocess.run(
                ['python', '-c', code],
                input=user_input,  # Pass user input to the subprocess
                capture_output=True,
                text=True,
                timeout=10  # Adjust timeout as needed
            )

            output = process.stdout.strip()
            error = process.stderr.strip()
        except subprocess.TimeoutExpired:
            error = "Code execution timed out"
        except Exception as e:
            error = str(e)

    return render(request, 'ide.html', {'code': code, 'output': output, 'error': error, 'user_input': user_input})

@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        owner = User.objects.get(username = request.user.username)
        project = Project.objects.create(name = name, owner = owner)
        project.save()
        return redirect('create_file', project_id=project.id)
    else:
        return render(request, 'create_project.html')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html',context)

@login_required
def create_file(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        file = File.objects.create(project=project, name=name, content=content)
        file.save()
        return redirect('file_detail', file.id)
    else:
        return render(request, 'create_file.html', {'project': project})

@login_required
def file_detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)

    # Get lexer based on file content type (you might need to adjust this)
    lexer = get_lexer_by_name('python', stripall=True)

    # Highlight the code using Pygments
    highlighted_code = highlight(file.content, lexer, HtmlFormatter())

    # Get CSS styles for syntax highlighting
    css_styles = HtmlFormatter(style='colorful').get_style_defs('.highlight')

    context = {
        'file': file,
        'highlighted_code': highlighted_code,
        'css_styles': css_styles
    }
    return render(request, 'file_detail.html', context)


@login_required
def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    return redirect('profile_page')

@login_required
def update_code(request,code_id):
    file = get_object_or_404(File,pk=code_id)
    if request.method == 'POST':
        file.content = request.POST.get('content')
        file.save()
        return redirect('home')
    return render(request,'update_file.html',{'file':file})

def about_us(request):
    return render(request,'about_us.html')