from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your Mlmodels here.

class Address(models.Model):
    streetNb = models.IntegerField()
    AptFloor = models.CharField(max_length=200)
    city = models.CharField(max_length=60)

    def __str__(self):
        return str(self.streetNb) + ', ' + self.AptFloor + ' - ' + self.city


class CommonInfo(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    birth_date = models.DateField(null=True)
    sex = models.CharField(max_length=10, choices=SEX, null=True)
    cin = models.CharField(max_length=15, null=True)
    phone_nb = models.CharField(max_length=30, null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    objects = models.Manager()

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        abstract = True


class Nurse(CommonInfo):
    salary = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)


class Doctor(CommonInfo):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    SPECIALTY = (
        ('General practice', 'General practice'),
        ('Clinical radiology', 'Clinical radiology'),
        ('Anaesthesia', 'Anaesthesia'),
        ('Ophthalmology', 'Ophthalmology')
    )
    email = models.EmailField()
    pwd = models.CharField(max_length=200)
    salary = models.FloatField()
    specialty = models.CharField(max_length=200, choices=SPECIALTY)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    objects = models.Manager()


# Insurance :
class InsuranceAgency(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_nb = models.CharField(max_length=30)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    repayment_rate = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])

    def __str__(self):
        return self.name


class InsuranceAccount(models.Model):
    insur_acc_nb = models.CharField(max_length=60)
    insuranceAgency = models.ForeignKey(
        InsuranceAgency,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.insur_acc_nb)


class Patient(CommonInfo):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    insur_acc_nb = models.OneToOneField(InsuranceAccount, null=True, on_delete=models.SET_NULL)
    weight = models.IntegerField(validators=[
        MaxValueValidator(200),
        MinValueValidator(1)
    ], null=True)
    allergies = models.CharField(max_length=200, null=True)


class Document(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    link = models.URLField()
    image = models.ImageField(null=True)
    patient = models.ForeignKey(
        Patient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='documents'
    )
    doctor = models.ForeignKey(
        Doctor,
        null=True,
        on_delete=models.SET_NULL
    )
    observation = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.title) + ' : ' + self.patient.__str__()


class Appointment(models.Model):
    day = models.DateField(u'Day of the appointment', help_text=u'Day of the appointment')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    patient = models.ForeignKey(
        Patient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='appointments'
    )
    APPOINTMENT_STATES = (
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Canceled', 'Canceled'),
    )
    state = models.CharField(max_length=20, choices=APPOINTMENT_STATES, default='Canceled', null=True)
    SPECIALTY = (
        ('General practice', 'General practice'),
        ('Clinical radiology', 'Clinical radiology'),
        ('Anaesthesia', 'Anaesthesia'),
        ('Ophthalmology', 'Ophthalmology')
    )
    specialty = models.CharField(max_length=200, choices=SPECIALTY, null=True)
    consulted = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Appointment'
        verbose_name_plural = u'Appointments'

    def __str__(self):
        return 'Appointment for : ' + self.patient.__str__() + ' at : ' + str(self.day) + \
               ', from ' + str(self.start_time) + ' to ' + str(self.end_time)

    def get_title(self):
        return self.patient.__str__() + ' - ' + str(self.start_time) + ' to ' + str(self.end_time)

    def check_overlap(self, event2_start2, event2_end):
        overlap = False
        if event2_start2 == self.end_time or event2_end == self.start_time:
            overlap = False
        elif (self.start_time <= event2_start2 <= self.end_time) or (self.start_time <= event2_end <= self.end_time):
            overlap = True
        elif event2_start2 <= self.start_time and event2_end >= self.end_time:
            overlap = True
        return overlap

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending time must be less than starting time')
        appointments = Appointment.objects.filter(day=self.day).exclude(id=self.id)
        if appointments.exists():
            for appointment in appointments:
                if self.check_overlap(appointment.start_time, appointment.end_time):
                    raise ValidationError('Please choose another time. Appointments are full at : ' + str(appointment.day) +
                                          ', ' + str(appointment.start_time) + '-' + str(appointment.end_time))


    @property
    def confirm_html_url(self):
        url = reverse('confirm_appointment', kwargs={'appointment_id': self.id})
        btn=''
        if self.state == 'Confirmed':
            btn = ""
        else:
            btn = f"<a style='color:white;'  class='btn btn-success' href='{url}'> Confirm appointment </a>"
        return btn

    @property
    def validate(self):
        url = reverse('validate_appointment', args=(self.id,))
        if self.state == 'Confirmed' and self.consulted is False:
            return f" <a style='color:white;' class='btn btn-success' href='{url}'> Consult </a>"
        elif self.state == 'Confirmed' and self.consulted:
            consul = Consultation.objects.filter(appointment=self)
            consulId = consul[0].id
            consultation_details_url = reverse('consultation_details', args=(consulId,))
            return f" <a style='color:white;' class='btn btn-success' href='{consultation_details_url}'> Consultation details </a>"
        else:
            return ""

class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    observation = models.CharField(max_length=200)

    def __str__(self):
        return 'Consultation nb°' + str(self.id)


class Bill(models.Model):
    PAYMENT_STATE = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    )
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    payment_state = models.CharField(max_length=10, choices=PAYMENT_STATE)
    consultation = models.OneToOneField(Consultation, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'Bill nb°' + str(self.id)


class Prescription(models.Model):
    consultation = models.OneToOneField(Consultation, null=True, on_delete=models.CASCADE)
    treatment = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'Prescription nb°' + str(self.id)