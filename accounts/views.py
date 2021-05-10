from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth


# Create your views here.
from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password', False)
        password2 = request.POST.get('password2', False)

        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exist')
                    return redirect('register')
                else:
                    # register user
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    # 1. login after register
                    # auth.login(request,user)
                    # messages.success(request, "you are now logged In")
                    # return redirect('index')

                    # 2. another method
                    user.save()
                    messages.success(request, 'You are now registered and able to login')
                    return redirect('login')

        else:
            messages.error(request, "password do not match")
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')

            return redirect('dashboard')

        else:
            messages.error(request, "Invalid credentials")

    else:
        return render(request, template_name='login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "you are now logged out")
    return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'dashboard.html', context)
