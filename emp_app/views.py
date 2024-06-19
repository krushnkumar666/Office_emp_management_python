from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        if first_name and last_name and salary and bonus and phone and dept and role:
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=int(salary),
                bonus=int(bonus),
                phone=int(phone),
                dept_id=int(dept),
                role_id=int(role),
                hire_date=datetime.now()
            )
            new_emp.save()
            return HttpResponse('Employee added successfully')
        else:
            return HttpResponse('Missing fields in form')

    elif request.method == 'GET':
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse("An error occurred")

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Please enter a valid emp_id")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept_id=dept)
        if role:
            emps = emps.filter(role_id=role)

        context = {
            'emps': emps,
            'departments': Department.objects.all(),
            'roles': Role.objects.all(),
            'name': name,
            'dept': dept,
            'role': role
        }
        return render(request, 'filter_emp.html', context)

    elif request.method == 'GET':
        context = {
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, 'filter_emp.html', context)

    else:
        return HttpResponse("An error occurred")
