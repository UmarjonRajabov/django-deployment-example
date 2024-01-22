# calc/urls.py
from django.urls import path
from .views import upload_excel, success_page , view_kpis,login_view ,excel_content

urlpatterns = [
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('success_page/', success_page, name='success_page'),
    path('view_kpis/', view_kpis, name='view_kpis'),
    path('login/', login_view, name='login'),
    path('excel_content/', excel_content, name='excel_content'),
]

# # kpi_project/urls.py
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#
# ]
