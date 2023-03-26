from django.shortcuts import render,redirect

from login.models import User


def index(request):
    pass
    return render(request,'login/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        # print("password and username",password, username)
        if username and password:
            user = User.objects.filter(name=username, password=password).first()
            if user:
                return redirect('/index/')
            else:
                message = "密码错误"
                return render(request, 'login/login.html', {'message': message})
        else:
            message = "错误信息"
            return render(request, 'login/login.html', {'message': message})
    return render(request,'login/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        if password2 != password1:
            message = "密码不一致"
            return render(request, 'login/login.html', {'message': message})
        else:
            if username and password1:
                exist_user = User.objects.filter(name=username).first()
                if exist_user:
                    message = "用户已存在"
                    return render(request, 'login/login.html', {'message': message})
                else:
                    user = User(name=username,password=password1)
                    user.save()
                    return redirect('/index/')
            else:
                message = "密码错误"
                return render(request, 'login/login.html', {'message': message})

    return render(request,'login/register.html')


def logout(request):
    pass
    return redirect('/login/')