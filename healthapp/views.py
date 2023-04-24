from django.http import HttpResponse
from .models import MedicalRecord, Doctor, Patient, Appointment, Payment
from .serializers import MedicalRecordSerializer, DoctorSerializer, \
    PatientSerializer, PaymentSerializer
from .serializers import AppointmentSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from reportlab.pdfgen import canvas


class AppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class PatientList(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


class PatientDetail(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


class PatientCreate(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PatientUpdate(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def put(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class PatientDelete(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def delete(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        patient.delete()
        return Response(status=204)


class DoctorsView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorList(APIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request):
        doctor = Doctor.objects.all()
        serializer = DoctorSerializer(doctor, many=True)
        return Response(serializer.data)


class DoctorDetail(APIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, patient_id):
        doctor = Doctor.objects.get(id=patient_id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


class DoctorCreate(APIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DoctorUpdate(APIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def put(self, request, patient_id):
        doctor = Doctor.objects.get(id=patient_id)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class DoctorDelete(APIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def delete(self, request, patient_id):
        doctor = Doctor.objects.get(id=patient_id)
        doctor.delete()
        return Response(status=204)


class MedicalRecordList(APIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get(self, request):
        med_record = MedicalRecord.objects.all()
        serializer = MedicalRecordSerializer(med_record, many=True)
        return Response(serializer.data)


class MedicalReportDetail(APIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get(self, request, patient_id):
        med_record = MedicalRecord.objects.get(id=patient_id)
        serializer = MedicalRecordSerializer(med_record)
        return Response(serializer.data)


class MedicalReportCreate(APIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MedicalReportUpdate(APIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def put(self, request, patient_id):
        med_record = MedicalRecord.objects.get(id=patient_id)
        serializer = MedicalRecordSerializer(med_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MedicalRecordDelete(APIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def delete(self, request, patient_id):
        med_record = MedicalRecord.objects.get(id=patient_id)
        med_record.delete()
        return Response(status=204)


class PaymentView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create a new payment record
        payment = Payment.objects.create(
            amount=serializer.validated_data['amount'],
            transaction_id=serializer.validated_data['transaction_id'],
        )

        # Update the payment status
        payment.status = 'completed'
        payment.save()

        # Return the serialized payment data
        return Response(self.serializer_class(payment).data)


class PaymentSlipView(APIView):
    serializer_class = PaymentSerializer

    def get(self, request, transaction_id, format=None):
        # Get the payment record
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate the PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payment_slip_{transaction_id}.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 750, "Payment Slip")
        p.drawString(100, 700, f"Transaction ID: {payment.transaction_id}")
        p.drawString(100, 650, f"Amount: {payment.amount}")
        p.drawString(100, 600, f"Status: {payment.status}")
        p.showPage()
        p.save()

        return response


class AppointmentList(APIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get(self, request):
        appointment_record = Appointment.objects.all()
        serializer = AppointmentSerializer(appointment_record, many=True)
        return Response(serializer.data)


class AppointmentDetail(APIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get(self, request, appointment_id):
        appointment_record = Appointment.objects.get(id=appointment_id)
        serializer = AppointmentSerializer(appointment_record)
        return Response(serializer.data)


class AppointmentCreate(APIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AppointmentUpdate(APIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def put(self, request, appointment_id):
        appointment_record = Appointment.objects.get(id=appointment_id)
        serializer = AppointmentSerializer(appointment_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class AppointmentDelete(APIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def delete(self, request, appointment_id):
        appointment_record = Appointment.objects.get(id=appointment_id)
        appointment_record.delete()
        return Response(status=204)
