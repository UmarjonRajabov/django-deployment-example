# calc/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import upload_excel, success_page, view_kpis, login_view, access_denied, kpi_card, kpi_index
from django.urls import path
from .views import KPIListCreateView, KPIRetrieveUpdateDestroyView, KPIArchiveListCreateView, KPIArchiveDetailView, EmployeeDetailAPIView

urlpatterns = [
    path('kpis/', KPIListCreateView.as_view(), name='kpi-list'),
    path('kpis/<int:pk>/', KPIRetrieveUpdateDestroyView.as_view(), name='kpi-detail'),
    path('employee-detail/<int:pk>/', EmployeeDetailAPIView.as_view()),
    path('kpi-archives/', KPIArchiveListCreateView.as_view(), name='kpi-archive-list'),
    path('kpi-archives/<int:pk>/', KPIArchiveDetailView.as_view(), name='kpi-archive-detail'),
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('success_page/', success_page, name='success_page'),
    path('view_kpis/', view_kpis, name='view_kpis'),
    # Authentication URLs
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('access_denied/', access_denied, name='access_denied'),
    path('kpi/index/', kpi_index, name='kpi_index'),
    path('kpi/card/', kpi_card, name='kpi_card'),
]
