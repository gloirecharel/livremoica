from django.shortcuts import render
from django.urls import reverse  # corrigé ici
from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import UserInfo

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

# Si ce fichier n’existe pas encore, crée-le, sinon commente cette ligne temporairement
from bookzilla.misc import anonymous_required


@login_required
def logout(request):
    djlogout(request)
    return render(request, 'registration/logout.html')


@anonymous_required
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or reverse('users:home')

        user = authenticate(username=username, password=password)
        if user is not None:
            djlogin(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, 'The username or password you entered is incorrect')
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


@login_required
def home(request):
    return render(request, 'users/home.html')



@anonymous_required
def register(request):
    if request.method == 'POST':
        message = ''
        # Récupération automatique des champs du formulaire
        username = request.POST.get('username')
        email    = request.POST.get('email')
        address  = request.POST.get('address')
        password = request.POST.get('password')

        # Les champs prénom, nom, date de naissance sont optionnels ou à générer automatiquement si besoin
        fname    = request.POST.get('firstName', '')
        lname    = request.POST.get('lastName', '')
        dob      = request.POST.get('dob', None)

        if User.objects.filter(username=username).exists():
            message = 'name_taken'
        elif User.objects.filter(email=email).exists():
            message = 'email_taken'

        if not message:
            try:
                new_user = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=fname, last_name=lname
                )
                # Si dob non fourni, on laisse null (champ nullable)
                new_user_info = UserInfo(user=new_user, address=address)
                if dob:
                    new_user_info.dob = dob
                new_user_info.save()
                # Ne connecte plus automatiquement, on affiche un message de succès côté front
            except Exception as e:
                print(str(e))
            message = "no_error"
        # Si requête AJAX, retourne le message, sinon redirige avec message
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(message)
        if message == "no_error":
            messages.success(request, "Votre compte a été créé avec succès. Connectez-vous !")
            return HttpResponseRedirect(reverse('users:login'))
        elif message == "name_taken":
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
        elif message == "email_taken":
            messages.error(request, "Cet email est déjà utilisé.")
        return render(request, 'registration/register.html')
    else:
        return render(request, 'registration/register.html')
    


def borrowed_books(request):
    return render(request, 'bookrequests/borrowed.html')

def lent_books(request):
    return render(request, 'bookrequests/lent.html')

