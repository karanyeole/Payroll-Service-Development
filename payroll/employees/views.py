from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm, EmployeeForm, HRForm, LeaveForm, SalaryJobTypeForm,PayrollForm
from .models import Employee, HR, Leave,Payroll
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from smtplib import SMTPAuthenticationError
from django.db.models import ExpressionWrapper, F, DurationField,Sum



def signup_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()
    return render(request, 'signup_employee.html', {'user_form': user_form, 'employee_form': employee_form})

def signup_hr(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        hr_form = HRForm(request.POST)
        if user_form.is_valid() and hr_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            hr = hr_form.save(commit=False)
            hr.user = user
            hr.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserForm()
        hr_form = HRForm()
    return render(request, 'signup_hr.html', {'user_form': user_form, 'hr_form': hr_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if hasattr(request.user, 'employee'):
        return redirect('employee_dashboard')
    elif hasattr(request.user, 'hr'):
        return render(request, 'hr_dashboard.html')

@login_required
def employee_dashboard(request):
    if hasattr(request.user, 'employee'):
        leave_requests = Leave.objects.filter(employee=request.user.employee)
        return render(request, 'employee_dashboard.html', {'leave_requests': leave_requests})
    return redirect('dashboard')

@login_required
def show_employees(request):
    if hasattr(request.user, 'hr'):
        employees = Employee.objects.filter(hr=request.user.hr)
        return render(request, 'show_employees.html', {'employees': employees})
    return redirect('dashboard')

@login_required
def change_employee_status(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.user.hr == employee.hr:
        if employee.status == 'inactive':
            employee.status = 'active'
        else:
            employee.status = 'inactive'
        employee.save()
    return redirect('show_employees')

@login_required
def apply_leave(request):
    if request.method == 'POST':
        leave_form = LeaveForm(request.POST)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            return redirect('employee_dashboard')
    else:
        leave_form = LeaveForm()
    return render(request, 'apply_leave.html', {'leave_form': leave_form})

@login_required
def calculate_total_leave_days(request):
    if hasattr(request.user, 'employee'):
        employee = request.user.employee
        today = timezone.localdate()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        # Calculate total leave days for the current month
        total_leave_days = Leave.objects.filter(
            employee=employee,
            status='Approved',
            start_date__lte=end_of_month,
            end_date__gte=start_of_month
        ).annotate(
            duration=ExpressionWrapper(
                F('end_date') - F('start_date') + timedelta(days=1),
                output_field=DurationField()
            )
        ).aggregate(total_days=Sum('duration'))

        total_days = total_leave_days['total_days'].days if total_leave_days['total_days'] else 0
        return render(request, 'total_leave_days.html', {'total_leave_days': total_days})
    return redirect('dashboard')

@login_required
def show_leave_requests(request):
    if hasattr(request.user, 'hr'):
        leave_requests = Leave.objects.filter(employee__hr=request.user.hr)
        return render(request, 'show_leave_requests.html', {'leave_requests': leave_requests})
    return redirect('dashboard')

@login_required
def manage_leave_request(request, leave_id, decision):
    leave = get_object_or_404(Leave, id=leave_id)
    if hasattr(request.user, 'hr'):
        if decision == 'approve':
            leave.status = 'Approved'
        elif decision == 'reject':
            leave.status = 'Rejected'
        leave.save()
        send_leave_status_email(leave, request.user.username)
    return redirect('show_leave_requests')

def send_leave_status_email(leave, hr_name):
    if leave.status == 'Approved':
        subject = "Leave Request Approved"
        template_name = 'email/leave_approved_email.html'
    else:
        subject = "Leave Request Rejected"
        template_name = 'email/leave_rejected_email.html'
    
    context = {
        'employee_name': leave.employee.user.username,
        'leave': leave,
        'hr_name': hr_name,
    }

    message = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Static email as the sender
        [leave.employee.user.email]
    )
    email.attach_alternative(message, "text/html")
    email.send()
    
def add_salary_job_type(request):
    if request.method == 'POST':
        form = SalaryJobTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with the name of the success URL or page
    else:
        form = SalaryJobTypeForm()
    return render(request, 'add_salary_job_type.html', {'form': form})

def calculate_payroll(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']

            today = timezone.localdate()
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            # Calculate total leave days for the current month
            total_leave_days = Leave.objects.filter(
                employee=employee,
                status='Approved',
                start_date__lte=end_of_month,
                end_date__gte=start_of_month
            ).annotate(
                duration=ExpressionWrapper(
                    F('end_date') - F('start_date') + timedelta(days=1),
                    output_field=DurationField()
                )
            ).aggregate(total_days=Sum('duration'))

            total_leave_days_count = total_leave_days['total_days'].days if total_leave_days['total_days'] else 0

            # Call the calculate_payroll method from LeaveManager
            payroll = Leave.objects.calculate_payroll(employee, total_leave_days_count)
            return render(request, 'payroll_success.html', {'payroll': payroll})
    else:
        form = PayrollForm()
    return render(request, 'calculate_payroll.html', {'form': form})


@login_required
def show_payroll_details(request):
    employee = request.user.employee

    # Get all payroll records for the employee
    payrolls = Payroll.objects.filter(employee=employee).order_by('-month')

    context = {
        'payrolls': payrolls,
    }

    return render(request, 'payroll_details.html', context)

def home(request):
    return render(request, 'home.html')
