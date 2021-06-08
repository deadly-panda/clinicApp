from calendar import HTMLCalendar
from datetime import timedelta, datetime
import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Appointment, Patient

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Create daily calendar, by hour
    def formathour(self, day, specialty=None):
        now = datetime.time(9, 0, 0)
        hours = [(datetime.datetime.combine(datetime.date(1, 1, 1), now) + datetime.timedelta(hours=i)).time() for i in range(11)]
        appointments_per_day = Appointment.objects.filter(day__day=day.day, specialty__iexact=specialty)

        if specialty is not None:
            appointments_per_day = Appointment.objects.filter(day__day=day.day, specialty__iexact=specialty)
        else:
            appointments_per_day = Appointment.objects.filter(day__day=day.day)

        d = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        d += f"<tr><th class='day' colspan='7'>{day.strftime('%A')} {day.day}-{day.month}-{day.year}</th></tr>"
        for i in range(len(hours)-1):
            d += f"<tr><td style='width:5px;' id='hour'><span class='date'>{hours[i]}</span></td>"
            flag = False
            for appoint in appointments_per_day:
                if appoint.check_overlap(hours[i], hours[i+1]):
                    d += f"<td style='background-color:#659EC7;  text-align:center; font-size:18px;'> {appoint.validate} {appoint.confirm_html_url}</td></tr>"
                else:
                    flag=True
            if flag:
                d += "</tr>"

        return d

    def formathour_forPatient(self, day, patient):
        now = datetime.time(9, 0, 0)
        hours = [(datetime.datetime.combine(datetime.date(1, 1, 1), now) + datetime.timedelta(hours=i)).time() for i in range(11)]
        pat = get_object_or_404(Patient, pk=patient.id)
        appointments_per_day = pat.appointments.filter(day__day=day.day)

        d = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        d += f"<tr><th class='day' colspan='7'>{day.strftime('%A')} {day.day}-{day.month}-{day.year}</th></tr>"
        for i in range(len(hours)-1):
            d += f"<tr><td style='width:5px;' id='hour'><span class='date'>{hours[i]}</span></td>"
            flag = False
            for appoint in appointments_per_day:
                if appoint.check_overlap(hours[i], hours[i+1]):
                    d += f"<td style='background-color:#659EC7;  text-align:center; font-size:18px;'> {appoint.state}</td></tr>"
                else:
                    flag=True
            if flag:
                d += "</tr>"

        return d

    # Return a day as a table cell.
    def formatday(self, day, appointments):
        appointments_per_day = appointments.filter(day__day=day)
        d = ''
        if appointments_per_day:
            theday = str(self.year)+'-'+str(self.month)+'-'+str(day)
            url = reverse('calendar_byday') + '?day='+theday
            d += f"<a href='{url}'>View all</a>"
        if day != 0:
            return f"<td class='date'><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, appointments):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, appointments)
        return f'<tr> {week} </tr>'

    def formatmonth(self, specialty=None, withyear=True):
        if specialty is not None:
            appointments = Appointment.objects.filter(day__year=self.year, day__month=self.month, specialty__iexact=specialty)
        else:
            appointments = Appointment.objects.filter(day__year=self.year, day__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, appointments)}\n'
        return cal

    def formatmonth_forPatient(self, patient, withyear=True):
        pat = get_object_or_404(Patient, pk=patient.id)
        appointments = pat.appointments.filter(day__year=self.year, day__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, appointments)}\n'
        return cal
