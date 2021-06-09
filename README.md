# Medical Clinic managment and diagnosis assistance web application

This repository is an web application to help a medical clinic with  their day-to-day managment.
It gives the possibility  for a patient to make an appointment & view his documents (bills, prescriptions, ultrasound-images.etc).
It also helps the doctors both with their schedules and diagnosis.
Finally, it presents dashboards giving the admins insights about different & important aspects of managment.

It was made with love and Django~=3.1.

# Steps to run  the project.
- Clone the project : ``` git clone https://github.com/deadly-panda/clinicApp.git ```
- Go to the project directory
- Create a Virtual Environment : ``` python -m venv myVenv ```
- Activate the virtual environment : ``` source myVenv/bin/activate ```
- Install requirements : ``` pip install -r requirements.txt ```
- Migrate : ``` python3 manage.py migrate ```
- Run the project : ``` python3 manage.py runserver ```

- You can also create a superuser to have admin permissions : ``` python3 manage.py createsuperuser ```


# The Classes

<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/3wNuMua.png" height="100%" width="100%" title="hover text">
</p> 

# Three types of users
# Patients
The patients can easly send an appointment request with the day & time they prefer & also the speciality of the doctor(general medecine, Ophthalmology..), view their prescriptions, bills & pay them, and most importantly have 24/7 access to their documents like x-ray 
shots or ultrasound images.

<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/PbNBCas.png" height="100%" width="100%" title="hover text">
</p> 


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/5NmJpCV.png" height="100%" width="100%" title="hover text">
</p> 


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/rqLwCil.png" height="100%" width="100%" title="hover text">
</p> 


# Doctors
The doctors recieve view their schedules, appointments requests  & decide wether to accept or decline, a notifications is then sent to the patient asking for the
appointment. In addition they can manage their patients information, add prescriptions, bills & important documents.
The web application not only help with basic managment of the doctors schedules, but also helps with diagnosis. For now, it can help predict weather a patient might 
have a cardiovascular diseas from relational data like age, sexe & cholesterol level, Also, classify chest x-ray images as images with pneumonia or not.
Other machine learning &  deep learning models could be easly integrated with the web application.


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/xFk8rnT.png" height="100%" width="100%" title="hover text">
</p> 


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/s8pAADT.png" height="100%" width="100%" title="hover text">
</p> 


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/vas7ybr.png" height="100%" width="100%" title="hover text">
</p> 

# Admins
Admins have total access to the web application and all the information, they can add, modify or archive any entity like doctors, nurses, patients, prescriptions..etc.
They also have a simple yet elegant dashboard, giving them insight about diffrent aspects like the ratio of paid/unpaid bills, appointments state distribution, patient
sex distribution also information about insurrance companies & accounts..etc.

<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/8Gm2QrF.png" height="100%" width="100%" title="hover text">
</p> 


<p align="center">
  <label style="font-weight: bold;">Categories</label>
  <img src="https://i.imgur.com/YMd2YoN.png" height="100%" width="100%" title="hover text">
</p> 





