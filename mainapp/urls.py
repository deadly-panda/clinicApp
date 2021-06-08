from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.homePage, name='home'),
    path('fillPatientDetails/', views.fillPatientDetails, name='fillPatientDetails'),

    path('list_entities/<str:entity>', views.list_entities, name='list_entities'),
    path('patient/<int:pk>', views.patient, name='patient'),
    path('patientDocs/<str:entity>', views.patientDocs, name='patientDocs'),
    path('bill/<int:idbill>', views.bill, name='bill'),
    path('prescription/<int:idprescription>', views.prescription, name='prescription'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard2/', views.dashboard2, name='dashboard2'),


    path('update/<int:pk>/<str:entity>', views.update_entities, name='update'),
    path('update_bp/<int:pk>/<str:entity>', views.update_bills_prescriptions, name='update_bp'),
    path('update_doc/<int:pk>/<int:idpatient>', views.update_documents, name='updateDoc'),
    path('create/<str:entity>', views.create_entities, name='create'),
    path('create_document/<int:idpatient>', views.create_document, name='create_document'),
    path('delete/<int:pk>/<str:entity>', views.delete_entities, name='delete'),
    path('delete_doc/<int:pk>/<int:idpatient>', views.delete_documents, name='deleteDoc'),

    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^calendar_byday/$', views.CalendarByDayView.as_view(), name='calendar_byday'),
    url(r'^appointment/new/$', views.appointment, name='appointment_new'),
    url(r'^confirm_appointment/(?P<appointment_id>\d+)/$', views.confirm_appointment, name='confirm_appointment'),

    url(r'^validate_appointment/(?P<appointment_id>\d+)/$', views.validate_appointment, name='validate_appointment'),

    url('doctorConsultations', views.doctorConsultations, name='doctorConsultations'),
    path('consultation_details/<int:pk>/', views.consultation_details, name='consultation_details'),

    path('malaria_diagnose/<int:id_document>/<int:idpatient>', views.malaria_diagnose, name='malaria_diagnose')
]
