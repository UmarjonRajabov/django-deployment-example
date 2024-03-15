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
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def extract_month(excel_file):
    # Assume the file name contains the month information, e.g., "january_data.xlsx"
    file_name = excel_file.file.name
    month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                   'november', 'december']
    for month_name in month_names:
        if month_name in file_name.lower():
            return month_names.index(month_name) + 1  # Adding 1 to match Python's month numbering (1-12)
    # If no month name found, default to the current month
    return datetime.now().month


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
                # Extract month from file name or content
                month = extract_month(excel_file)
                # Store data in the database with the month information
                process_data_and_calculate_kpis(excel_content, month)
            except pd.errors.EmptyDataError:
                # Handle empty Excel file
                return render(request, 'upload_excel.html', {'form': form, 'error_message': 'Empty Excel file'})
            return redirect('success_page')

    else:
        form = ExcelFileForm()

    return render(request, 'upload_excel.html', {'form': form})


# 2. Archive Previous Months
# You can implement this logic in a separate function or as part of process_data_and_store_kpis.
def archive_previous_months():
    # Calculate the start and end dates for the previous month
    today = datetime.now()
    last_month_end = datetime(today.year, today.month, 1) - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1)

    # Query KPI entries for the previous month
    previous_month_kpis = KPI.objects.filter(month__gte=last_month_start, month__lte=last_month_end)

    # Move the data to the archive
    kpi_archive_entries = []
    for kpi_entry in previous_month_kpis:
        kpi_archive_entry = KPIArchive.objects.create(
            user=kpi_entry.user,
            employee=kpi_entry.employee,
            month=kpi_entry.month,
            performance_score=kpi_entry.performance_score,
            # Copy other fields as needed
        )
        kpi_archive_entries.append(kpi_archive_entry)

    # Delete or mark the original KPI entries as archived
    # previous_month_kpis.delete()  # Delete entries from the original table
    # Or, mark them as archived if you want to keep them in the original table
    previous_month_kpis.update(archived=True)


# Call this function before storing new data for the current month
archive_previous_months()


# 3. Display Data According to Current Month
# In your view_kpis view:

def success_page(request):
    return render(request, 'success_page.html')


def create_KPIs_for_group(group, user, month):
    print(f"Processing group: {group}")
    kpis_to_create = []
    for index, row in group.iterrows():
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

        # Check if the employee exists for the user
        employee, created = Employee.objects.update_or_create(
            user=user,
            defaults={
                'name': row.get('Имя_сотрудника_или_кандидата', ''),
                'position': row.get('ДОЛЖНОСТЬ', ''),
                'branch': row.get('ФИЛИАЛ_ГО', ''),
                'division': row.get('ОПЕРУ_БХМ_БХО', ''),
                'department': row.get('ПОДРАЗДЕЛЕНИЕ', ''),
                'table_number': row.get('ТАБЕЛЬ', ''),
                'fixed': row.get('ОКЛАД_РАБОТНИКА_СУМ', ''),
            },
            create_defaults={
                'name': row.get('Имя_сотрудника_или_кандидата', ''),
                'position': row.get('ДОЛЖНОСТЬ', ''),
                'branch': row.get('ФИЛИАЛ_ГО', ''),
                'division': row.get('ОПЕРУ_БХМ_БХО', ''),
                'department': row.get('ПОДРАЗДЕЛЕНИЕ', ''),
                'table_number': row.get('ТАБЕЛЬ', ''),
                'start': row.get('Начала', ''),
                'end': row.get('Конец', ''),
                'fixed': row.get('ОКЛАД_РАБОТНИКА_СУМ', ''),
            }
        )

        # Try to get an existing employee for the user

        kpi = KPI(
            user=user,
            employee=employee,
            month=month,  # Use the provided month
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
            start=row.get('Начала', ''),
            end=row.get('Конец', ''),

        )
        kpis_to_create.append(kpi)
    KPI.objects.bulk_create(kpis_to_create)
    print(f"Created {len(kpis_to_create)} KPIs for user {user.username} and month {month}")


def process_data_and_calculate_kpis(data_frame, month):
    print("Column names in DataFrame:", data_frame.columns)
    print(data_frame)  # Add this line to print the DataFrame
    print(data_frame.head())  # Print the first few rows of the DataFrame
    if 'Definition' in data_frame.columns:
        if 'Username' in data_frame.columns:
            grouped_df = data_frame.groupby('Username')
            for name, group in grouped_df:
                try:
                    user = CustomUser.objects.get(username=name)
                except ObjectDoesNotExist:
                    print(f"User with username '{name}' does not exist. Skipping KPI creation.")
                    continue  # Skip processing for this row

                print(f"Processing group {name}")

                create_KPIs_for_group(group, user, month)
        else:
            print("Column 'username' not found in the DataFrame.")
    else:
        print("Column 'Definition' not found in the DataFrame.")


# 3. Display Data According to Current Month
# In your view_kpis view:
@login_required
def view_kpis(request):
    # Initialize photo_url
    photo_url = None

    # Get the current month
    current_month = datetime.now().month

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

    # Retrieve KPI entries for the current month
    print("Photo URL:", photo_url)
    if request.user.is_staff:
        kpi_entries = KPI.objects.filter(month__month=current_month)
    else:
        employee = get_object_or_404(Employee, user=request.user)
        kpi_entries = KPI.objects.filter(employee=employee, month__month=current_month)

    # Render the template with the photo_url included in the context
    return render(request, 'view_kpis.html', {'kpi_entries': kpi_entries, 'photo_url': photo_url})


def access_denied(request):
    return render(request, 'access_denied.html')


def kpi_index(request):
    return render(request, 'kpi/index.html')


def kpi_card(request):
    return render(request, 'kpi/card.html')

# 4. Allow Users to View Previous Months
# You can implement a dropdown menu or any other UI element in your template
# to allow users to select and view data for previous months.
