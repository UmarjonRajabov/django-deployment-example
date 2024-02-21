# calc/views.py
import os
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
from django.conf import settings


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


    else:
        form = ExcelFileForm()

    return render(request, 'upload_excel.html', {'form': form})


def success_page(request):
    return render(request, 'success_page.html')

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
                try:
                    employee = Employee.objects.get(user=user)
                except Employee.DoesNotExist:
                    employee = None

                if not employee:
                    # Create a new Employee object if it doesn't exist
                    employee = Employee.objects.create(
                        user=user,
                        name=row.get('Имя_сотрудника_или_кандидата', ''),
                        position=row.get('ДОЛЖНОСТЬ', ''),
                        branch=row.get('ФИЛИАЛ_ГО', ''),
                        division=row.get('ОПЕРУ_БХМ_БХО', ''),
                        department=row.get('ПОДРАЗДЕЛЕНИЕ', ''),
                        table_number=row.get('ТАБЕЛЬ', ''),
                        start=row.get('Начала', ''),
                        end=row.get('Конец', ''),
                    )
                # employee, created = Employee.objects.get_or_create(
                #     user=user,
                #     name=row.get('Имя_сотрудника_или_кандидата', ''),
                #     position=row.get('ДОЛЖНОСТЬ', ''),
                #     branch=row.get('ФИЛИАЛ_ГО', ''),
                #     division=row.get('ОПЕРУ_БХМ_БХО', ''),
                #     department=row.get('ПОДРАЗДЕЛЕНИЕ', ''),
                #     table_number=row.get('ТАБЕЛЬ', ''),
                #     start=row.get('Начала', ''),
                #     end=row.get('Конец', ''),
                #
                #     # name=row['Имя_сотрудника_или_кандидата'],
                #     # position=row['ДОЛЖНОСТЬ'],
                #     # Add other relevant fields
                # )
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


@login_required
def view_kpis(request):
    # Initialize photo_url
    photo_url = None

    # print("User:", request.user)
    if hasattr(request.user, 'employee'):
        print("Employee:", request.user.employee)
        if hasattr(request.user.employee, 'table_number'):
            table_number = request.user.employee.table_number
            photo_filename = f"{table_number}.jpg"
            photo_url = settings.MEDIA_URL + 'employee_photos/' + photo_filename
        else:
            print("Employee has no table_number attribute")
    else:
        print("User has no employee attribute")

    # Retrieve KPI entries as needed
    # print("Photo URL:", photo_url)
    if request.user.is_staff:
        kpi_entries = KPI.objects.all()
    else:
        employee = get_object_or_404(Employee, user=request.user)
        kpi_entries = KPI.objects.filter(employee=employee)

    # Render the template with the photo_url included in the context
    return render(request, 'view_kpis.html', {'kpi_entries': kpi_entries, 'photo_url': photo_url})


def access_denied(request):
    return render(request, 'access_denied.html')


def kpi_index(request):
    return render(request, 'kpi/index.html')


def kpi_card(request):
    return render(request, 'kpi/card.html')


# def read_excel_data(file_path):
#     # Read the Excel file into a pandas DataFrame
#     df = pd.read_excel(file_path)
#
#     # Process the data as needed
#     labels = df['Month'].tolist()
#     data = df['Value'].tolist()
#
#     # Prepare the data to be passed to the template
#     chart_data = {
#         'labels': labels,
#         'data': data,
#     }
#
#     return chart_data


# def your_view(request):
#     # Assuming 'excel_file_path' is the path to your Excel file
#     excel_file_path = '/path/to/your/excel/file.xlsx'
#
#     # Read Excel data and prepare it for the template
#     chart_data = read_excel_data(excel_file_path)
#
#     # Pass the chart data to the template context
#     context = {
#         'chart_data': chart_data,
#     }
#
#     return render(request, 'view_kpis.html', context)