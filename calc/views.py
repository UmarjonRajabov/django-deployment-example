# calc/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExcelFileForm
from .models import Employee, KPI, CustomUser
import pandas as pd
from datetime import datetime
from django.shortcuts import get_object_or_404
from .utils import process_excel_file
from .models import ExcelFile


# def excel_content(request):
#     file_id = request.GET.get('file_id')
#     if file_id:
#         excel_file = ExcelFile.objects.get(pk=file_id)
#         excel_content = pd.read_excel(excel_file.file.path)
#         return render(request, 'excel_content.html',
#                       {'excel_content': excel_content, 'file_path': excel_file.file_path()})
#     else:
#         return render(request, 'excel_content.html', {'excel_content': None, 'file_path': None})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')  # Replace 'dashboard' with your desired redirect URL
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


@staff_member_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save(commit=False)
            excel_file.uploaded_by = request.user
            excel_file.save()
            try:
                excel_content = pd.read_excel(excel_file.file.path)
            except pd.errors.EmptyDataError:
                # Handle empty Excel file
                return render(request, 'upload_excel.html', {'form': form, 'error_message': 'Empty Excel file'})

            # Process the data and calculate KPIs
            process_data_and_calculate_kpis(excel_content)

            return redirect('success_page')
            # print(f"File path: {excel_file.file.path}")
            # return redirect('success_page')
            # excel_file = form.cleaned_data['excel_file']
            # process_excel_file(excel_file)
            # excel_file = request.FILES['excel_file']
            # df = pd.read_excel(excel_file)
            # #
            # # # Process the data and calculate KPIs
            # process_data_and_calculate_kpis(df)

            # return redirect('success_page')

    else:
        form = ExcelFileForm()

    return render(request, 'upload_excel.html', {'form': form})


def success_page(request):
    return render(request, 'success_page.html')


# def process_data_and_calculate_kpis(data_frame):
#     # Implement your KPI calculation logic here
#     # You can iterate through the data_frame and calculate KPIs for each employee
#     pass
# update this function

def process_data_and_calculate_kpis(data_frame):
    print("Column names in DataFrame:", data_frame.columns)
    print(data_frame)  # Add this line to print the DataFrame
    print(data_frame.head())  # Print the first few rows of the DataFrame
    if 'Definition' in data_frame.columns:
        if 'Username' in data_frame.columns:
            for index, row in data_frame.iterrows():
                print(f"Processing row {index}: {row}")
                performance_score = row['ПЛАН']
                kpi_name = row['KPI_name']
                metric = row['Единица']
                fact = row['ФАКТ']
                finished = row['ИСПОЛНЕНИЕ']
                premium = row['Functional']
                definition = row['Definition']
                method = row['Метод_расчота']
                weight = row['Вес_показателья']
                activity = row['Активность']
                overall = row['Общий_KPI']
                username = row['Username']

                # Save KPI to the database (adjust the fields based on your models)
                # user=request.user
                # employee = Employee.objects.create(
                #     user=user,
                #     name=row['Имя_сотрудника_или_кандидата'],
                #     position=row['ДОЛЖНОСТЬ'],
                #     # Add other relevant fields
                # )
                # Try to get an existing employee for the user
                user = CustomUser.objects.get(username=username)
                employee, created = Employee.objects.get_or_create(
                    user=user,
                    name=row.get('Имя_сотрудника_или_кандидата', ''),
                    position=row.get('ДОЛЖНОСТЬ', ''),
                    branch=row.get('ФИЛИАЛ_ГО', ''),
                    division=row.get('ОПЕРУ_БХМ_БХО', ''),
                    department=row.get('ПОДРАЗДЕЛЕНИЕ', ''),
                    table_number=row.get('ТАБЕЛЬ', ''),
                    salary=row.get('ОКЛАД_РАБОТНИКА_СУМ', ''),
                    start=row.get('Начала', ''),
                    end=row.get('Конец', ''),

                    # name=row['Имя_сотрудника_или_кандидата'],
                    # position=row['ДОЛЖНОСТЬ'],
                    # Add other relevant fields
                )
                KPI.objects.create(
                    employee=employee,
                    month=datetime.now(),  # Update with actual month from the Excel file
                    performance_score=row['ПЛАН'],
                    kpi_name=row['KPI_name'],
                    metric=row['Единица'],
                    fact=row['ФАКТ'],
                    finished=row['ИСПОЛНЕНИЕ'],
                    premium=row['Functional'],
                    definition=row['Definition'],
                    method=row['Метод_расчота'],
                    weight=row['Вес_показателья'],
                    activity=row['Активность'],
                    overall=row['Общий_KPI'],
                    # performance_score=performance_score,
                    # kpi_name=kpi_name,
                    # metric=metric,
                    # fact=fact,
                    # finished=finished,
                    # premium=premium,
                    # definition=definition,
                    # method=method,
                    # weight=weight,
                    # activity=activity,
                    # overall=overall,
                    # Add other KPI-related fields
                )

        else:
            print("Column 'username' not found in the DataFrame.")
    else:
        print("Column 'Definition' not found in the DataFrame.")


# def view_kpis(request):
#     kpis = KPI.objects.all()
#     return render(request, 'view_kpis.html', {'kpis': kpis})
@login_required
def view_kpis(request):
    if request.user.is_staff:
        kpi_entries = KPI.objects.all()  # Retrieve KPI entries as needed
        print(kpi_entries)
    else:
        user = request.user
        # kpi_entries = KPI.objects.filter(employee__user=user)
        employee = get_object_or_404(Employee, user=user)
        kpi_entries = KPI.objects.filter(employee=employee)

    return render(request, 'view_kpis.html', {'kpi_entries': kpi_entries})
    # return redirect('access_denied')  # Redirect to an access denied page or another appropriate view


def access_denied(request):
    return render(request, 'access_denied.html')


def kpi_index(request):
    return render(request, 'kpi/index.html')


def kpi_card(request):
    return render(request, 'kpi/card.html')
