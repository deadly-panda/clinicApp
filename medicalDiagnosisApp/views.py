from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import numpy as np
from keras.preprocessing import image as photos
from keras.models import load_model

# Create your views here.
model=load_model('medicalDiagnosisApp/Mlmodels/DengueorMalariaVgg19model.h5')


def index(request):
    context={}
    return render(request, 'medicalDiagnosisApp/index.html', context)

def malaria_diagnose(request):
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    test_img = 'medicalDiagnosisApp/media/' + filePathName.split('/')[3]
    img = photos.load_img(test_img, target_size=(224, 224))
    x = photos.img_to_array(img)
    x = x / 255
    x = x.reshape(1, 224, 224, 3)
    predi = model.predict(x)
    labelId = np.argmax(predi[0])
    label = 'Parasite' if labelId==0 else 'Uninfected'
    context = {'filePathName': filePathName, 'label': label}
    return render(request, 'medicalDiagnosisApp/index.html', context)

def pneumonia_diagnose(request):
    context = {}
    return render(request, 'medicalDiagnosisApp/index.html', context)
