from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from media import fonctions
import media


# Create your views here.
from media.fonctions import hash_fichier
from media import signature1
from media.verification import verifier


def index(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(first_name)
        print(last_name)
        print(username)
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username taken')
                messages.info(request, 'Username taken')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                print('Email taken')
                messages.info(request, 'Email taken')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('User created')
                messages.info(request, 'User Created')
                return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        print(password1)
        print(username)
        user = auth.authenticate(username=username, password=password1)
        print('user', user)
        if user is not None:
            auth.login(request, user)
            print("login successful")
            messages.info(request, 'login successful')
            print('login', User.is_authenticated)
            return render(request, 'upload.html')
            #return redirect('register')
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        upload_file = request.FILES['document']
        print(upload_file)
        fs = FileSystemStorage()
        name = fs.save(upload_file.name, upload_file)
        context['url'] = fs.url(name)
        context['name']=upload_file.name
        print('Document saved')
        messages.info(request, 'document saved')
        print(context['url'])
        sign = signature(request, upload_file)
        context['sign'] = sign[4]
        return render(request, 'upload.html', context)
    else:
        return render(request, 'upload.html')


def signature(request,upload_file):
    listex = []
    listey = []
    kerr=2
    caracteres = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
    texte1 = hash_fichier(upload_file.name)
    fichier = upload_file.name
    print('texte1',texte1)
    liste_signature = signature1.signer(caracteres, texte1, kerr, listex, listey,fichier)
    return liste_signature


def verification(request):
    context = {}
    if request.method == 'POST':
        file1 = request.FILES['file1']
        file2=request.FILES['file2']
        print("Premier fichier",file1)
        print("Fichier de signature", file2)
        fs = FileSystemStorage()
        name1 = fs.save(file1.name, file1)
        context['url1'] = fs.url(name1)
        context['f_name1']=file1.name
        print('Document 1 saved')
        fs = FileSystemStorage()
        name2 = fs.save(file2.name, file2)
        context['url2'] = fs.url(name2)
        context['f_name2'] = file2.name
        print('Document 2 saved')
        messages.info(request, 'document saved')
        print(context['url1'])
        print(context['url2'])
        check_bool = verifier(file1.name, file2.name)
        if check_bool:
            context['verif']="Le fichier est authentique"
        else:
            context['verif'] = "Le fichier est n'est pas authentique"
        return render(request, 'check.html', context)
    else:
        return render(request, 'check.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')


