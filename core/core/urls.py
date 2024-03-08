
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/',views.employee_page, name='employee'),
    path('',views.resume_page,name='resume'),
    path('generate/<int:employee_id>', views.generate_resume, name='generate'),
    path('download/<int:employee_id>', views.download_resume, name='download'),
    
]
