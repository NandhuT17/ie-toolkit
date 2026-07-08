from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Operator, Machine, TimeStudy
from .forms import OperatorForm, MachineForm, TimeStudyForm
import qrcode
from django.http import HttpResponse
import openpyxl # type: ignore
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import string


def register_user(request) :
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords doesn't match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        else :
            user = User.objects.create_user(
                username = username,
                email = email,
                password = password1,
            )
            login(request,user)
            messages.success(request,"You are logged in successfully")
            return redirect('dashboard')

    return render(request,'base/register.html')


def login_page(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("dashboard")
        except User.DoesNotExist:
            pass
    return render(request, "base/login.html")


def logout_user(request) :
    logout(request)
    return redirect('dashboard')


def dashboard(request):
    return render(request, "base/dashboard.html")


@login_required
def operators(request):
    form = OperatorForm()
    if request.method == "POST":
        form = OperatorForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            token = form.cleaned_data["token_id"]
            if Operator.objects.filter(name=name, token_id=token).exists():
                messages.error(
                    request,
                    "Operator with this Name and Token ID already exists."
                )
            else:
                operator = form.save()
                qr = qrcode.make(operator.token_id)
                filename = f"{operator.name}_{operator.token_id}.png"
                qr.save("media/qr_codes/" + filename)
                operator.qr_code = "qr_codes/" + filename
                operator.save()
                messages.success(request, "Operator added successfully.")
                return redirect("operators")
    operators_list = Operator.objects.all().order_by("id")
    paginator = Paginator(operators_list, 10)
    page_number = request.GET.get("page")
    operators = paginator.get_page(page_number)
    context = {
        "operators" : operators,
        "form" : form,
    }
    return render(request, "base/operators.html", context)


@login_required
def machines(request):
    form = MachineForm()
    if request.method == "POST":
        form = MachineForm(request.POST)
        if form.is_valid():
            machine = form.cleaned_data["machine_model"]
            if Machine.objects.filter(machine_model=machine).exists():
                messages.error(request, "Machine already exists.")
            else:
                form.save()
                messages.success(request, "Machine added successfully.")
                return redirect("machines")
    machines = Machine.objects.all()
    context = {
        "form": form,
        "machines": machines
    }
    return render(request, "base/machines.html", context)


@login_required
def time_study(request):
    token = request.GET.get("token")
    operator = None
    if token:
        try:
            operator = Operator.objects.get(token_id=token)
        except Operator.DoesNotExist:
            operator = None
    form = TimeStudyForm()
    form.fields["machine"].queryset = Machine.objects.order_by("machine_model")
    if request.method == "POST":
        form = TimeStudyForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            total = (
                study.reading1 +
                study.reading2 +
                study.reading3 +
                study.reading4 +
                study.reading5
            )
            study.average = total / 5
            study.capacity = 3600 / study.average
            study.save()
            return redirect("time_study")
    numbers = range(1, 201)
    context = {
        "form": form,
        "operator": operator,
        "numbers": numbers,
    }
    return render(request, "base/time_study.html", context)



def history(request):
    selected_date = request.GET.get("date")
    if selected_date:
        studies = TimeStudy.objects.filter(date=selected_date)
    else:
        studies = TimeStudy.objects.all()
    context = {
        "studies": studies,
        "selected_date": selected_date,
        "batches": list(string.ascii_uppercase)
    }
    return render(request, "base/history.html", context)


def export_excel(request):
    selected_date = request.GET.get("date")
    batch = request.GET.get("batch")
    target = float(request.GET.get("target"))
    batch = request.GET.get("batch")
    target = request.GET.get("target")
    studies = TimeStudy.objects.filter(
        batch_no=batch,
        date=selected_date
    )
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Time Study"
    sheet.append([
        "Date",
        "Operator",
        "Token ID",
        "Machine",
        "Batch",
        "Operation",
        "Reading 1",
        "Reading 2",
        "Reading 3",
        "Reading 4",
        "Reading 5",
        "Average",
        "Allowance",
        "Capacity",
        "Target",
        "Difference",
        "Efficiency(%)"
    ])
    batch_name = "Report"

    for study in studies:
        batch_name = study.batch_no
        target_value = float(target)
        difference = study.capacity - target_value
        if target_value != 0:
            efficiency = (study.capacity / target_value) * 100
        else:
            efficiency = 0
        sheet.append([
            study.date,
            study.operator.name,
            study.operator.token_id,
            study.machine.machine_model,
            study.batch_no,
            study.operation,
            study.reading1,
            study.reading2,
            study.reading3,
            study.reading4,
            study.reading5,
            study.average,
            study.allowance,
            round(study.capacity),
            target,
            round(difference),
            round(efficiency)
        ])
    filename = f"{batch}_{selected_date}.xlsx"
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    workbook.save(response)
    return response


def get_operator(request):
    token = request.GET.get("token")
    try:
        operator = Operator.objects.get(token_id=token)
        return JsonResponse({
            "id": operator.id,
            "name": operator.name,
            "token": operator.token_id
        })
    except Operator.DoesNotExist:
        return JsonResponse({
            "error": "Operator not found"
        })