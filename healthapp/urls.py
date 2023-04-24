from django.urls import path
from .api import RegisterApi
from .views import PatientList, PatientDetail, PatientCreate, PatientUpdate, \
    AppointmentView, \
    DoctorsView, PatientDelete, DoctorList, DoctorDetail, DoctorCreate, DoctorUpdate, DoctorDelete, MedicalRecordList, \
    MedicalReportDetail, MedicalReportCreate, MedicalReportUpdate, MedicalRecordDelete, PaymentView, PaymentSlipView, \
    AppointmentList, AppointmentDetail, AppointmentCreate, AppointmentUpdate, AppointmentDelete

urlpatterns = [
    # ...
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterApi.as_view()),

    path('api/patients/', PatientList.as_view()),
    path('api/patients-detail/<int:patient_id>/', PatientDetail.as_view()),
    path('api/patients/create/', PatientCreate.as_view()),
    path('api/patients/<int:patient_id>/update/', PatientUpdate.as_view()),
    path('api/patients/<int:patient_id>/delete/', PatientDelete.as_view()),

    path('api/doctors/', DoctorList.as_view()),
    path('api/doctor-detail/<int:doctor_id>/', DoctorDetail.as_view()),
    path('api/doctor/create/', DoctorCreate.as_view()),
    path('api/doctor/<int:doctors_id>/update/', DoctorUpdate.as_view()),
    path('api/doctor/<int:doctor_id>/delete/', DoctorDelete.as_view()),

    path('api/medrecord/', MedicalRecordList.as_view()),
    path('api/medrecord-detail/<int:med_record_id>/', MedicalReportDetail.as_view()),
    path('api/medrecord/create/', MedicalReportCreate.as_view()),
    path('api/medrecord/<int:med_record_id>/update/', MedicalReportUpdate.as_view()),
    path('api/medrecord/<int:med_record_id>/delete/', MedicalRecordDelete.as_view()),

    path('api/appointment/', AppointmentList.as_view()),
    path('api/appointment-detail/<int:appointment_record_id>/', AppointmentDetail.as_view()),
    path('api/appointment/create/', AppointmentCreate.as_view()),
    path('api/appointment/<int:appointment_record_id>/update/', AppointmentUpdate.as_view()),
    path('api/appointment/<int:appointment_record_id>/delete/', AppointmentDelete.as_view()),

    path('api/payments/', PaymentView.as_view()),
    path('api/payments/<str:transaction_id>/slip/', PaymentSlipView.as_view()),
]
