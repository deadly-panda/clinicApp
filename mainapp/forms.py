from django.forms import ModelForm, DateInput, DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'id_username'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password'}))


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'birth_date', 'sex', 'cin', 'email',
                  'phone_nb', 'specialty', 'salary')

class NurseForm(ModelForm):
    class Meta:
        model = Nurse
        fields = ('first_name', 'last_name', 'birth_date', 'sex', 'cin',
                  'phone_nb', 'salary')

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'birth_date', 'sex', 'cin',
                  'email', 'phone_nb', 'weight', 'allergies')

class InsuranceAgencyForm(ModelForm):
    class Meta:
        model = InsuranceAgency
        fields = ('name', 'email', 'phone_nb', 'repayment_rate')

class InsuranceAccountForm(ModelForm):
    class Meta:
        model = InsuranceAccount
        fields = '__all__'


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'type', 'link', 'image', 'observation')


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        widgets = {
            'day': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d'),
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%H:%M'),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%H:%M'),
        }
        fields = ('day', 'start_time', 'end_time', 'specialty')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['day'].input_formats = ('%Y-%m-%d',)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)

class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('fee', 'payment_state')


class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ('treatment',)


class ConsulationForm(ModelForm):
    class Meta:
        model = Consultation
        fields = ('observation',)