from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate,login,logout

from users.forms import UserRegisterForm,UserLoginForm




def UserRegisterView(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')

    else :
        form=UserRegisterForm()

    return render(request,'users/register.html',{'form':form})


def UserLoginView(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(
                request,username=username,password=password
            )
            if user is not None:
                    login(request, user)
                    return redirect('home') 
            else:
                form.add_error(None, "Username yoki parol xato!")
    else:
            form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def UserLogoutView(request):
     logout(request)

     return redirect('login')



# home page uchun
def home_view(request):
    return render(request, 'home.html')