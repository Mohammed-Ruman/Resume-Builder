from django.shortcuts import render
from .models import Employee, Project, Skills
from django.contrib import messages
from django.urls import reverse

from django.http import FileResponse, HttpResponse
from datetime import datetime

import pdfkit

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')



def employee_page(request):
    if request.method != 'POST':
        return render(request, 'employee.html')
    
    # Extract employee data
    employee_name = request.POST.get('name')
    designation = request.POST.get('designation')
    summary = request.POST.get('summary')
    # Create or update employee object
    employee, created = Employee.objects.get_or_create(name=employee_name, defaults={'designation': designation, 'summary': summary})

    # Extract skills data
    programming = request.POST.get('programming')
    framework = request.POST.get('framework')
    dev_tools = request.POST.get('dev_tools')
    web_tools = request.POST.get('web_tools')
    op_sys = request.POST.get('op_sys')
    ver_tools = request.POST.get('ver_tools')
    skills, created = Skills.objects.get_or_create(employee=employee, defaults={'programming': programming, 'framework': framework, 'dev_tools': dev_tools, 'web_tools': web_tools, 'op_sys': op_sys, 'ver_tools': ver_tools})

    # Extract projects data
    projects_data = []
    for i in range(len(request.POST.getlist('project_name[]'))):
        project_name = request.POST.getlist('project_name[]')[i]
        project_description = request.POST.getlist('project_description[]')[i]
        role_res = request.POST.getlist('role_res[]')[i]
        tech_used = request.POST.getlist('tech_used[]')[i]
        projects_data.append({'project_name': project_name, 'project_description': project_description, 'role_res': role_res, 'tech_used': tech_used})

    # Create or update project objects
    for project_data in projects_data:
        project, created = Project.objects.get_or_create(project_name=project_data['project_name'], defaults={'project_description': project_data['project_description'], 'role_res': project_data['role_res'], 'tech_used': project_data['tech_used']})
        employee.projects.add(project)
    messages.success(request,"Employee Details Saved Successfully!")
    return render(request, 'employee.html')

def resume_page(request):
    employees = Employee.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        employees = Employee.objects.filter(name__icontains=search) | Employee.objects.filter(id__icontains=search)
    return render(request, 'resume.html', {'employees': employees})

def generate_resume(request, employee_id):
    # Get employee data and generate resume content
    employee = Employee.objects.get(id=employee_id)
    skill = Skills.objects.get(employee=employee)
    projects = employee.projects.all()

    for project in projects:
        role=project.role_res.split('●')
        new_role = [r.strip() for r in role if len(r)>0]
        project.role_res=new_role

    context={
        'employee':employee,
        'skill':skill,
        'projects':projects
    }

    # Return the file path
    return render(request,'pdftemplate.html',context)

def download_resume(request, employee_id):
    
    today = datetime.now()
    formatted_date = today.strftime('%d%m%Y')

    employee = Employee.objects.get(id=employee_id)
    pdf_filename = f"resume_{employee.name}_{formatted_date}.pdf"

    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('generate',args=[employee_id])),False,configuration=config)

    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    return response