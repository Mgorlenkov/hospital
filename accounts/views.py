from itertools import count
import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from panel.models import Otdel, People, Profile
from docxtpl import DocxTemplate
from docx import Document
import pandas as pd

from .forms import *

# "Вот эта часть кода моя." Хотеля бы я так сказать, но все здесь сделано
# нанятым мной программистом. Я лишь немного помогал разобраться с некоторыми вопросами,
# в частности с чтением кириллицы из екселя с помощью пакета xlrd. Мой же код находится в репозитории hospPyQT.
# В нем я пытался сделать нечто похожее в десктопном приложении на PyQT, пока не понял что стороннюю программу на
# рабочем компьютере не запустить. И там, конечно, с чистотой кода полная ж... 

# Изначально я обратился к заведующей с просьбой спросить у IT-отдела нужен ли им хостинг с VPS сервером, с этим сервисом, оплаченный 
# оплаченный еще на пару месяцев под какие-либо больничные проекты или просто как тестовую площадку. 
# Независимо от вашего решения, могу предоставить вам доступ к нему, если посчитаете, что он вам пригодится.  

def index(req):
    # filters
    room = -1
    
    if 'selectSubmit' in req.POST:
        data = req.POST
        print(data)

        pacients = []
        for el in data:
            if data[el] == 'selectedPacient':
                pacients.append(el)
        return manyGen(req, pacients)

    if 'bedTablet' in req.POST:
        data = dict(req.POST)
        data_to_doc = {}

        data_out = []
        for el in data:
            if 'id: ' in el:
                d = {}
                d['nIb'] = data[el][0]
                d['name'] = data[el][1]
                d['date'] = data[el][2]

                data_out.append(d)

        return downloadMany(data_out)

    if 'glik' in req.POST:
        data = dict(req.POST)

        data_out = []
        for el in data:
            if 'id: ' in el:
                data_out.append(data[el])
        return glikProfileManyGen(req, data_out)

    if 'water' in req.POST:
        data = dict(req.POST)

        data_out = []
        for el in data:
            if 'id: ' in el:
                data_out.append(data[el])
        return waterManyGen(req, data_out)

    if req.method == 'POST' and 'excel' in req.FILES:
        myfile = req.FILES['excel']
        fs = FileSystemStorage()
        filename = fs.save('media/' + myfile.name, myfile)
        excel = pd.read_excel(r'media/' + myfile.name, sheet_name=0, header=4, engine='xlrd')

        data = excel.to_dict()

        colunms = ['ФИО', '№ ИБ', 'Палата', 'Дата госпитализации']
        persons = People.objects.all()
        names = []
        nIbs = []
        dates = []
        room_numbers = []
        for i, column in enumerate(colunms):
            for index in data[column]:
                if  str(data['№ ИБ'][index]) != 'nan':
                    if i == 0:
                        names.append(data[column][index])
                    if i == 1:
                        nIbs.append(data[column][index])
                    if i == 2:
                        if str(data[column][index]) == 'nan':
                            room_numbers.append(0)
                        else:
                            room_numbers.append(data[column][index])
                    if i == 3:
                        dates.append(data[column][index])
        
        for people in persons:
            people.delete()

        for i, _name in enumerate(names):
            person = People.objects.filter(name = _name).all()
            if len(person):
                person = person[0]
                person.name = _name
                person.nIb = nIbs[i]
                person.date = dates[i]
                person.room = room_numbers[i]
                person.save()

            else:
                person = People()
                person.name = _name
                person.nIb = nIbs[i]
                person.date = dates[i]
                person.room = room_numbers[i]
                person.otdel = Otdel.objects.filter(id = Profile.objects.filter(user_id = req.user.id).all()[0].otdel_id).all()[0]
                person.save()
        fs.delete(filename)
        # os.remove('media/' + myfile.name)

    if req.method == 'POST' and 'room' in req.POST:
        room = int(req.POST['room'])

    form = ExcelIn()

    rooms = []
    for pacient in People.objects.all():
        if pacient.room not in rooms:
            rooms.append(pacient.room)

    try:
        if room != -1:
            return render(req, 'work/work.html', {
                'People': People.objects.filter(room = room).all(),
                'group': Profile.objects.filter(user_id = req.user.id).all()[0].otdel_id,
                'form': form,
                'rooms': rooms
            })
        else:
            return render(req, 'work/work.html', {
                'People': People.objects.all(),
                'group': Profile.objects.filter(user_id = req.user.id).all()[0].otdel_id,
                'form': form,
                'rooms': rooms
            })
    except:
        return render(req, 'work/work.html', {
            'People': People.objects.all(),
            'group': None,
            'form': form,
        })

def manyGen(req, pacients):

    peoples = []

    for pacient in pacients:
        people = People.objects.get(id = pacient)
        peoples.append(people)

    return render(req, 'work/manyBlank.html', 
    {
        'pacients': peoples
    })

def blank(req, id):
    print(id)
    return render(req, 'work/blank.html', {
        'pacient': People.objects.filter(nIb = id).all()[0]
    })

def combine_word_documents(name, files):
    merged_document = Document()

    for index, file in enumerate(files):
        sub_doc = Document(file)

        # Don't add a page break if you've reached the last file.
        if index < len(files)-1:
           sub_doc.add_page_break()

        for element in sub_doc.element.body:
            merged_document.element.body.append(element)
        
        os.remove(file)

    merged_document.save(f'{name}.docx')

def download(req, nIb):
    file_path = f"{nIb}.docx"
    pacient = People.objects.filter(nIb = nIb).all()[0]
    doc = DocxTemplate("bedTablet.docx")
    doc.render({
        "full_name": pacient.name,
        "id": pacient.nIb,
        "date": pacient.date
    })
    doc.save(file_path)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = f'inline; filename={nIb}.docx' + os.path.basename(file_path)
    os.remove(file_path)
    return response

def downloadMany(data):
    files = []

    for el in data:
        file_path = f"{el['nIb']}.docx"
        pacient = People.objects.filter(nIb = el['nIb']).all()[0]
        doc = DocxTemplate("bedTablet.docx")
        doc.render({
            "full_name": pacient.name,
            "id": pacient.nIb,
            "date": pacient.date
        })
        doc.save(file_path)
        files.append(file_path)

    combine_word_documents('bedTabletOut', files)

    with open('bedTabletOut.docx', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = f'inline; filename=bedTablet.docx'
    os.remove('bedTabletOut.docx')
    return response


def glikProfile(req, nIb):
    if req.method == 'POST':
        form = GlikProfileForm(req.POST)
        if form.is_valid():
            file_path = f"{nIb}.docx"
            doc = DocxTemplate("GlikProfile.docx")
            doc.render({
                "name0": form.cleaned_data['name'],
                "room0": form.cleaned_data['room'],
                "date0": form.cleaned_data['date']
            })
            doc.save(file_path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            os.remove(file_path)
            return response

    pacient = People.objects.filter(nIb = nIb).all()[0]

    form = GlikProfileForm(initial={'name': pacient.name, 'room': pacient.room})
    return render(req, 'work/glikProfile.html', {
        'form': form
    })


def glikProfileManyGen(req, data):

    if len(data) <= 4:
        data_to_doc = {}
        for i, people in enumerate(data):
            data_to_doc['name'+str(i)] = people[0]
            data_to_doc['room'+str(i)] = people[2]
            data_to_doc['date'+str(i)] = people[1]

        file_path = "glik.docx"
        doc = DocxTemplate("GlikProfile.docx")
        doc.render(data_to_doc)
        doc.save(file_path)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        os.remove(file_path)
        return response

    else:
        count = 0
        files = []
        for i, el in enumerate(data):
            if i % 4 == 0:
                count+=1
        
        for i in range(0, len(data), count+1):
            data_to_doc = {}
            list = data[i:i+4]
            for a, el in enumerate(list):
                data_to_doc[f'name{a}'] = el[0]
                data_to_doc[f'date{a}'] = el[1]
                data_to_doc[f'room{a}'] = el[2]

            file_path = f"glik{i}.docx"
            doc = DocxTemplate("GlikProfile.docx")
            doc.render(data_to_doc)
            doc.save(file_path)
            files.append(file_path)

        combine_word_documents('glik', files)
        with open('glik.docx', 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=glik.docx'
        os.remove('glik.docx')
        return response


def water(req, nIb):
    if req.method == 'POST':
        form = Water(req.POST)
        if form.is_valid():
            file_path = f"{nIb}.docx"
            doc = DocxTemplate("water.docx")
            doc.render({
                "last_name": form.cleaned_data['name'],
                "room": form.cleaned_data['room'],
                "date": form.cleaned_data['date']
            })
            doc.save(file_path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            os.remove(file_path)
            return response

    pacient = People.objects.filter(nIb = nIb).all()[0]

    form = GlikProfileForm(initial={'name': pacient.name, 'room': pacient.room})
    return render(req, 'work/glikProfile.html', {
        'form': form
    })


def waterManyGen(req, data):
    files = []
    data_to_doc = {}
    for i, people in enumerate(data):
        data_to_doc['last_name'] = str(people[0]).split(' ')[0]
        data_to_doc['room'] = people[2]
        data_to_doc['date'] = people[1]

        file_path = f"waterBalance{i}.docx"
        doc = DocxTemplate("water.docx")
        doc.render(data_to_doc)
        doc.save(file_path)
        files.append(file_path)
        
    combine_word_documents('waterBalance', files)
    with open('waterBalance.docx', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'inline; filename=waterBalance.docx'
    os.remove('waterBalance.docx')
    return response


def pinList(req, nIb):
    if req.method == 'POST':
        form = Pin(req.POST)
        if form.is_valid():
            true = u'\u22a0'
            false = u'\u2395'
            data = form.cleaned_data
            print(data)
            for el in data:
                if data[el] == True:
                    data[el] = u'\u22a0'
                elif data[el] == False:
                    data[el] = u'\u2395'
                elif isinstance(data[el], datetime.date):
                    data[el] = datetime.date.strftime(data[el], '%d.%m.%Y')

            if data['yes_no'] == true:
                data['yes'] = true
                data['no'] = false
            elif data['yes_no'] == false:
                data['yes'] = false
                data['no'] = true

            file_path = f"{nIb}.docx"
            doc = DocxTemplate("PIN-list.docx")
            doc.render(data)
            doc.save(file_path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            os.remove(file_path)
            return response

    pacient = People.objects.filter(nIb = nIb).all()[0]
    form = Pin(initial={'name': pacient.name, 'date': datetime.date.today()})
    return render(req, 'work/pinList.html', {
        'form': form
    })


def editPacient(req, id):
    pacient = People.objects.get(id = id)

    if req.POST:
        data = req.POST

        name = data['name']
        nIb = data['nIb']
        room = data['room']

        pacient.name = name
        pacient.nIb = nIb
        pacient.room = room

        pacient.save()
        return redirect('home')

    if pacient:
        return render(req, 'work/edit.html', 
        {
            'pacient': pacient
        })