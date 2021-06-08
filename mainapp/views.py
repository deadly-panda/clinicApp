from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


from .models import *
from .forms import *
from .decorators import *


from datetime import datetime, date, timedelta
import calendar
from .utils import Calendar
from django.views import generic

import numpy as np
from keras.preprocessing import image as photos

from keras.models import load_model
malariaModel=load_model('mainapp/Mlmodels/DengueorMalariaVgg19model.h5')

# Create your views here.


@unautheticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='patient')
            user.groups.add(group)
            Patient.objects.create(
                user=user,
            )
            login(request, user)
            return redirect('fillPatientDetails')
    context = {'form': form}
    return render(request, 'mainapp/register.html', context)


@unautheticated_user
def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                messages.info(request, 'Disabled account')
        else:
            messages.info(request, 'Invalid username or password !')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'mainapp/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @allowed_users(allowed_roles=['patient', 'doctor', 'admin'])
def homePage(request):
    context = {}
    return render(request, 'mainapp/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def fillPatientDetails(request):
    patient = request.user.patient
    address_form = AddressForm()
    insuranceAccount_form = InsuranceAccountForm()
    profile_form = PatientForm(instance=patient)
    if request.method == 'POST':
        profile_form = PatientForm(request.POST, instance=patient)
        address_form = AddressForm(request.POST)
        insuranceAccount_form = InsuranceAccountForm(request.POST)
        if all((profile_form.is_valid(), address_form.is_valid(), insuranceAccount_form.is_valid())):
            address = address_form.save()
            insuranceAccount = insuranceAccount_form.save()
            profile = profile_form.save(commit=False)
            profile.address = address
            profile.insur_acc_nb = insuranceAccount
            profile.save()
            return redirect('home')

    context = {'profile_form': profile_form, 'address_form': address_form, 'insuranceAccount_form': insuranceAccount_form}
    return render(request, 'mainapp/fillPatientDetails.html', context)


@allowed_users(allowed_roles=['admin', 'doctor'])
@login_required(login_url='login')
def list_entities(request, entity):
    if entity=='doctor':
        items_list = Doctor.objects.all().order_by('-created')
    elif entity=='nurse':
        items_list = Nurse.objects.all().order_by('-created')
    elif entity=='patient':
        items_list = Patient.objects.all()
    elif entity=='agency':
        items_list = InsuranceAgency.objects.all()
    elif entity=='bill':
        items_list = Bill.objects.all().order_by('-consultation__appointment__day')
    elif entity=='prescription':
        items_list = Prescription.objects.all().order_by('-consultation__appointment__day')

    paginator = Paginator(items_list, 2)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {'items': items, 'page': page}
    if entity=='agency':
        myurl = 'mainapp/entities/insurance_agencies.html'
    else:
        myurl = 'mainapp/entities/'+entity+'s.html'
    return render(request, myurl, context)
    # SpecialtyFilter = DoctorFilter(request.GET, queryset=doctors)
    # doctors = SpecialtyFilter.qs
    # context = {'doctors': doctors, 'SpecialtyFilter': SpecialtyFilter}


@allowed_users(allowed_roles=['admin'])
def update_entities(request, pk, entity):
    if entity == 'doctor':
        item = Doctor.objects.get(id=pk)
        form = DoctorForm(instance=item)
    elif entity == 'nurse':
        item = Nurse.objects.get(id=pk)
        form = NurseForm(instance=item)
    elif entity == 'patient':
        item = Patient.objects.get(id=pk)
        form = PatientForm(instance=item)
        insur_acc_nb = item.insur_acc_nb
        insur_acc_form = InsuranceAccountForm(instance=insur_acc_nb)
    elif entity == 'agency':
        item = InsuranceAgency.objects.get(id=pk)
        form = InsuranceAgencyForm(instance=item)


    address = item.address
    address_form = AddressForm(instance=address)
    if request.method == 'POST':
        if entity == 'doctor':
            form = DoctorForm(request.POST, instance=item)
        elif entity == 'nurse':
            form = NurseForm(request.POST, instance=item)
        elif entity == 'patient':
            form = PatientForm(request.POST, instance=item)
            insur_acc_form = InsuranceAccountForm(request.POST, instance=insur_acc_nb)
        elif entity == 'agency':
            form = InsuranceAgencyForm(request.POST, instance=item)
        address_form = AddressForm(request.POST, instance=address)
        if all((form.is_valid(), address_form.is_valid())):
            item = form.save(commit=False)
            address = address_form.save()
            item.address = address
            if entity=='patient' and insur_acc_form.is_valid():
                insur_acc = insur_acc_form.save()
                item.insur_acc_nb = insur_acc
            item.save()
            return redirect(list_entities, entity=entity)
    context = {'form': form, 'entity': entity, 'address_form': address_form}
    if entity=='patient':
        context['insur_acc_form']= insur_acc_form

    form_url = 'mainapp/forms/entity_form.html'
    return render(request, form_url, context)


@allowed_users(allowed_roles=['admin'])
def update_bills_prescriptions(request, pk, entity):
    if entity == 'bill':
        item = Bill.objects.get(id=pk)
        form = BillForm(instance=item)
    elif entity == 'prescription':
        item = Prescription.objects.get(id=pk)
        form = PrescriptionForm(instance=item)
    if request.method == 'POST':
        if entity == 'bill':
            form = BillForm(request.POST, instance=item)
        elif entity == 'prescription':
            form = PrescriptionForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect(list_entities, entity=entity)
    context = {'form': form, 'entity': entity}
    form_url = 'mainapp/forms/bp_form.html'  # bp : Bill Prescription
    return render(request, form_url, context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_entities(request, pk, entity):
    myurl = ''
    if entity == 'doctor':
        item = Doctor.objects.get(id=pk)
    elif entity == 'nurse':
        item = Nurse.objects.get(id=pk)
    elif entity == 'patient':
        item = Patient.objects.get(id=pk)
    elif entity == 'agency':
        item = InsuranceAgency.objects.get(id=pk)
    elif entity == 'bill':
        item = Bill.objects.get(id=pk)
    elif entity == 'prescription':
        item = Prescription.objects.get(id=pk)
    if request.method=='POST':
        #item.is_active=False;
        item.delete()
        return redirect(list_entities, entity=entity)
    context = {'myurl': myurl, 'item': item}
    return render(request, 'mainapp/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def create_entities(request, entity):
    if entity=='doctor':
        form = DoctorForm()
        userCreationform = UserCreationForm()
    elif entity == 'nurse':
        form = NurseForm()
    elif entity == 'agency':
        form = InsuranceAgencyForm()

    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if entity == 'doctor':
            form = DoctorForm(request.POST)
            userCreationform = UserCreationForm(request.POST)

        elif entity == 'nurse':
            form = NurseForm(request.POST)
        elif entity == 'agency':
            form = InsuranceAgencyForm(request.POST)

        if all((form.is_valid(), address_form.is_valid())):
            item = form.save(commit=False)
            if entity=='doctor':
                if userCreationform.is_valid():
                    user = userCreationform.save()
                    group = Group.objects.get(name='doctor')
                    user.groups.add(group)
                    item.user=user

            address = address_form.save()
            item.address = address
            item.save()
            return redirect(list_entities, entity=entity)
    context = {'form': form, 'address_form': address_form, 'entity': entity}
    if entity=='doctor':
        context['userCreationform'] = userCreationform

    return render(request, 'mainapp/forms/entity_form.html', context)


@login_required(login_url='login')
def patient(request, pk):
    pat = Patient.objects.get(id=pk)
    documents = pat.documents.all()
    context = {'patient': pat, 'documents': documents}
    return render(request, 'mainapp/entities/patient.html', context)


@allowed_users(allowed_roles=['patient'])
@login_required(login_url='login')
def patientDocs(request, entity):
    pat = request.user.patient
    if entity=='document':
        items_list = pat.documents.all()
    elif entity == 'insurance':
        items_list = [pat.insur_acc_nb]
    elif entity=='bill':
        appointments = pat.appointments.all().order_by('day')
        consultations = []
        bills = []
        for appoint in appointments:
            try:
                consul = Consultation.objects.filter(appointment=appoint)[0]
                consultations.append(consul)
            except:
                pass
        for consul in consultations:
            bill = Bill.objects.filter(consultation=consul)[0]
            bills.append(bill)
        items_list = bills
    elif entity=='prescription':
        appointments = pat.appointments.all().order_by('day')
        consultations = []
        prescriptions = []
        for appoint in appointments:
            try:
                consul = Consultation.objects.filter(appointment=appoint)[0]
                consultations.append(consul)
            except:
                pass
        for consul in consultations:
            prescription = Prescription.objects.filter(consultation=consul)
            prescriptions.append(prescription)
        items_list = prescriptions

    paginator = Paginator(items_list, 2)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {'items': items, 'page': page}
    myurl = 'mainapp/profile/my'+entity+'s.html'
    return render(request, myurl, context)


def bill(request, idbill):
    b = get_object_or_404(Bill, pk=idbill)
    context = {'bill': b}
    return render(request, 'mainapp/entities/bill.html', context)


def prescription(request, idprescription):
    presc = get_object_or_404(Prescription, pk=idprescription)
    context = {'prescription': presc}
    return render(request, 'mainapp/entities/prescription.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def create_document(request, idpatient):
    doc = request.user.doctor
    pat = get_object_or_404(Patient, pk=idpatient)
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.doctor = doc
            document.patient = pat
            document.save()
            return redirect(patient, pk=idpatient)
    context = {'form': form}
    return render(request, 'mainapp/forms/document_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def malaria_diagnose(request, id_document, idpatient):
    doc = get_object_or_404(Document, pk=id_document)
    img_name = doc.image.url.split('/')[3]
    img_path = 'mainapp/media/' + img_name
    img = photos.load_img(img_path, target_size=(224, 224))
    x = photos.img_to_array(img)
    x = x / 255
    x = x.reshape(1, 224, 224, 3)
    prediction = malariaModel.predict(x)
    labelId = np.argmax(prediction[0])
    label = 'Parasite' if labelId == 0 else 'Uninfected'
    context = {'document':doc, 'label': label, 'img_name': img_name}
    return render(request, 'medicalDiagnosis/MalariaDocumentDiagnosis.html', context)

'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def pneumonia_diagnose(request, id_document, idpatient):
    doc = get_object_or_404(Document, pk=id_document)
    img_name = doc.image.url.split('/')[3]
    img_path = 'mainapp/media/' + img_name
    img = photos.load_img(img_path, target_size=(224, 224))
    x = photos.img_to_array(img)
    x = x / 255
    x = x.reshape(1, 224, 224, 3)
    prediction = pneumoniaModel.predict(x)
    labelId = np.argmax(prediction[0])
    label = 'Parasite' if labelId == 0 else 'Uninfected'
    context = {'document':doc, 'label': label, 'img_name': img_name}
    return render(request, 'medicalDiagnosis/PneumoniaDocumentDiagnosis.html', context)
'''


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def update_documents(request, pk, idpatient):
    document = Document.objects.get(id=pk)
    form = DocumentForm(instance=document)
    if request.method=='POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(patient, pk=idpatient)
    context = {'form': form}
    return render(request, 'mainapp/forms/document_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def delete_documents(request, pk, idpatient):
    document = Document.objects.get(id=pk)
    if request.method=='POST':
        document.delete()
        return redirect(patient, pk=idpatient)
    return render(request, 'mainapp/delete_document.html', context={})


class CalendarView(generic.ListView):
    model = Appointment
    template_name = 'mainapp/appointments/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        user = self.request.user
        specialty = None
        html_cal = cal.formatmonth(specialty, withyear=True)
        try:
            specialty = user.doctor.specialty
            html_cal = cal.formatmonth(specialty, withyear=True)
        except:
            try:
                html_cal = cal.formatmonth_forPatient(user.patient, withyear=True)
            except:
                specialty = None
                html_cal = cal.formatmonth(specialty, withyear=True)

        context = {'calendar': mark_safe(html_cal), 'prev_month': prev_month(d), 'next_month': next_month(d)}
        return context


class CalendarByDayView(generic.ListView):
    model = Appointment
    template_name = 'mainapp/appointments/calendar_byday.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_day(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        user = self.request.user
        specialty = None
        html_cal = cal.formathour(d, specialty)
        try:
            specialty = user.doctor.specialty
            html_cal = cal.formathour(d, specialty)
        except:
            try:
                html_cal = cal.formathour_forPatient(d, user.patient)
            except:
                specialty = None
                html_cal = cal.formathour(d, specialty)

        context = {'calendar': mark_safe(html_cal), 'prev_day': prev_day(d), 'next_day': next_day(d)}
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_day(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.today()

def prev_day(d):
    prev_day = d - timedelta(days=1)
    day = 'day=' + str(prev_day.year) + '-' + str(prev_day.month) + '-' + str(prev_day.day)
    return day

def next_day(d):
    next_day = d + timedelta(days=1)
    day = 'day=' + str(next_day.year) + '-' + str(next_day.month) + '-' + str(next_day.day)
    return day


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def confirm_appointment(request, appointment_id=None):
    instance = Appointment()
    if appointment_id:
        instance = get_object_or_404(Appointment, pk=appointment_id)
        redirect_url = reverse('calendar_byday') + '?day=' + str(instance.day)
        if request.POST:
            instance.state = 'Confirmed'
            instance.save()
            return redirect(redirect_url)
    context = {'appointment': instance}
    return render(request, 'mainapp/appointments/confirm_appointment.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def appointment(request, appointment_id=None):
    form = AppointmentForm()
    if request.POST:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appoint = form.save(commit=False)
            appoint.patient = request.user.patient
            appoint.state = 'Pending'
            appoint.save()
            redirect_url = redirect_url = reverse('calendar_byday') + '?day=' + str(appoint.day)
            return redirect(redirect_url)
        else:
            return render(request, 'mainapp/appointments/appointment.html', {'form': form, 'error':ValidationError('Please choose another time. Appointments are full at : ' + str(form.cleaned_data['day']) +
                                          ', ' + str(form.cleaned_data['start_time']) + '-' + str(form.cleaned_data['end_time']) )})
    return render(request, 'mainapp/appointments/appointment.html', {'form': form})


@allowed_users(allowed_roles=['doctor'])
@login_required(login_url='login')
def doctorConsultations(request):
    doc = get_object_or_404(Doctor, id=request.user.doctor.id)
    items_list = Consultation.objects.filter(doctor=doc).order_by('-appointment__day')
    paginator = Paginator(items_list, 2)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {'items': items, 'page': page}
    myurl = 'mainapp/entities/doctorConsultations.html'
    return render(request, myurl, context)


@login_required()
@allowed_users(allowed_roles=['doctor'])
def validate_appointment(request, appointment_id=None):
    consulation_form = ConsulationForm()
    prescription_form = PrescriptionForm()
    bill_form = BillForm()
    if appointment_id:
        consultation = consulation_form.save(commit=False)
        appoint = get_object_or_404(Appointment, id=appointment_id)
        appoint.consulted = True
        appoint.save()
        consultation.appointment = appoint
        consultation.doctor = request.user.doctor
    else:
        consultation = Consultation()

    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        prescription_form = PrescriptionForm(request.POST)
        consulation_form = ConsulationForm(request.POST, instance=consultation)

        if all((bill_form.is_valid(), prescription_form.is_valid(), consulation_form.is_valid())):
            consultation = consulation_form.save(commit=False)
            bill = bill_form.save(commit=False)
            bill.consultation = consultation
            prescription = prescription_form.save(commit=False)
            prescription.consultation = consultation

            consultation.save()
            prescription.save()
            bill.save()

            return redirect('calendar')
    context = {'consulation_form':consulation_form, 'prescription_form':prescription_form, 'bill_form':bill_form}
    return render(request, 'mainapp/appointments/validate_appointment.html', context)


@login_required(login_url='login')
def consultation_details(request, pk):
    consul = Consultation.objects.get(id=pk)
    bill = Bill.objects.get(consultation=consul)
    prescription = Prescription.objects.get(consultation=consul)
    context = {'consultation': consul, 'bill': bill, 'prescription': prescription}
    return render(request, 'mainapp/entities/consultation_details.html', context)

def bill_payments_distribution(request):
    paid = Bill.objects.filter(payment_state='Paid').count()
    pending = Bill.objects.filter(payment_state='Pending').count()
    data = [paid, pending]
    labels = ['Paid', 'Pending']
    return {
        'labels': labels,
        'data': data,
    }

def sex_distribution(request):
    labels = ['Male', 'Female']
    m = Patient.objects.filter(sex='Male').count()
    f = Patient.objects.filter(sex='Female').count()
    data = [m, f]
    return {
        'labels': labels,
        'data': data,
    }

def specialty_distribution(request):
    labels = ['General practice', 'Clinical radiology', 'Anaesthesia', 'Ophthalmology']
    data = []
    for label in labels:
        data.append(Doctor.objects.filter(specialty=label).count())
    return {
        'labels': labels,
        'data': data,
    }

def appointment_state_distribution(request):
    labels = ['Confirmed', 'Pending', 'Canceled']
    data = []
    for label in labels:
        data.append(Appointment.objects.filter(state=label).count())
    return {
        'labels': labels,
        'data': data,
    }

@login_required(login_url='login')
def dashboard(request):
    context = {
        'bill_payments_distribution': bill_payments_distribution(request),
        'sex_distribution': sex_distribution(request),
        'specialty_distribution': specialty_distribution(request),
        'appointment_state_distribution': appointment_state_distribution(request),
    }
    return render(request, 'mainapp/dashboard.html', context)


def inssurance_repayment_rates(request):
    labels = []
    data = []
    QuerySet = InsuranceAgency.objects.all()
    for e in QuerySet:
        labels.append(e.name)
        data.append(e.repayment_rate)
    return {
        'labels': labels,
        'data': data,
    }

def inssurance_disstribution(request):
    QS = InsuranceAgency.objects.all()
    agencies = []
    labels = []
    data = []
    for e in QS:
        agencies.append(e.name)
    for ag in agencies:
        labels.append(ag)
        data.append(InsuranceAccount.objects.filter(insuranceAgency__name__contains=ag).count())

    return {
        'labels': labels,
        'data': data,
    }


@login_required(login_url='login')
def dashboard2(request):
    context = {
        'inssurance_repayment_rates': inssurance_repayment_rates(request),
        'inssurance_disstribution': inssurance_disstribution(request),
    }
    return render(request, 'mainapp/dashboard2.html', context)

