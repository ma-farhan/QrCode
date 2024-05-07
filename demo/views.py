
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.http import HttpResponse, HttpResponseServerError
from qrcode import make
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def encode(request):
    data = None  # Initialize data variable
    if request.method == 'POST':
        data = request.POST.get('data', '')  # Use get() method with default value

        # Validate and sanitize input if needed

        if data:
            try:
                img = make(data)
                img.save('demo/static/images/test.png')
            except Exception as e:
                # Handle potential errors during QR code creation
                return HttpResponseServerError("An error occurred while generating the QR code.")
    return render(request, 'home.html', {'data': data})

def SendData(request):
    # Your view logic here
    return HttpResponse("Sending Data...")

def index(request):
    return render(request,'index.html')


def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def register(request):
    if request.method=='POST':
        name=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:
            user=User.objects.create_user(username=name,email=email,password=password1)
            user.is_staff=True
            user.is_superuser=True
            user.save()
            messages.success(request,"your account has been created!")
            return redirect('login')
        else:
            messages.warning(request,"password mismatching!!.....")
            return redirect('register')
    else:
        form=CreateUserForm()
        return render(request, 'register.html',{'form':form})