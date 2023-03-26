from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
import hashlib
import re
from random import sample
from django.db.models.functions import ExtractYear
from django.db.models import Count
# Create your views here.

def sha256(key):
    sha256_key = hashlib.sha256()
    sha256_key.update(key.encode("utf-8"))
    return sha256_key.hexdigest()

def esg_index(request):
    status = request.COOKIES.get('is_login') # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的 cookie
    if not status:
        return redirect('/login/')
    return render(request, "index.html")

def searchstr(str,old_list):
    new_list=[]
    for item in old_list:        
        if re.search(str,item.title,re.I) is not None:
            new_list.append(item)
    return new_list

def esg_list(request): 
    global content
    global sort
    global tags
    global flag
    global search_report_list 
    if request.method == 'POST': 
        search_report_list = []
        content = request.POST.get('content')
        sort = request.POST.get('sort')
        tags = request.POST.getlist('tag')
        flag = 1
    else:
        flag = 0
        if not request.GET.get("page"):
            sample_list = sample(range(1, esg_reports.objects.count()), 20)
            search_report_list = list(esg_reports.objects.filter(id__in = sample_list).order_by('-edittime').all())
            content = 0

    if(flag == 1):
        source_list = ["cninfo","shse","szse"]
        site_list = []
        if len(tags):
            for tag in tags:
                site_list.append(source_list[int(tag)])
        else:
            site_list = source_list
        if sort == "re-time":
            search_report_list = list(esg_reports.objects.filter(site__in = site_list).order_by('-edittime').all())
        else:
            search_report_list = list(esg_reports.objects.filter(site__in = site_list).order_by('edittime').all())
        search_report_list = searchstr(content,search_report_list)

    current_num = int(request.GET.get("page", 1))
    paginator = Paginator(search_report_list, 20)
    page = paginator.page(current_num)
    page_obj = paginator.get_page(page)

    # 大于11页时
    if paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if current_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif current_num - 5 < 1:
            page_range = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            page_range = range(current_num - 5, current_num + 5 + 1)
    # 小于11页时显示所有页码
    else:
        page_range = paginator.page_range

    return render(request, "list.html", {"page": page, "page_obj": page_obj, "paginator": paginator, "current_num": current_num, "page_range": page_range, "content": content})

def esg_content(request,id):
    report = esg_reports.objects.get(id = id)
    return render(request, "content.html", {"report": report})

def esg_changelog(request):
    return render(request, 'changelog.html',)

def esg_about(request):
    return render(request, 'about.html',)

def esg_contact(request):
    return render(request, 'contact.html',)

def esg_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        # print("password and username",password, username)
        if username and password:
            user = User.objects.filter(name=username, password=sha256(password)).first()
            if user:
                rep = redirect("/index/")
                rep.set_cookie("is_login", True)
                return rep
            else:
                message = "Invalid username or password."
                return render(request, 'login.html', {'message': message})
        else:
            message = "Error: No username or password"
            return render(request, 'login.html', {'message': message})
    return render(request,'login.html',)

def esg_logout(request):
    rep = redirect('/login/')
    rep.delete_cookie("is_login")
    return rep

def esg_register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        if password2 != password1:
            message = "Passwords does not match"
            return render(request, 'register.html', {'message': message})
        else:
            if username and password1:
                exist_user = User.objects.filter(name=username).first()
                if exist_user:
                    message = "User already exists"
                    return render(request, 'register.html', {'message': message})
                else:
                    user = User(name=username,password=password1)
                    user.save()
                    return redirect('/index/')
            else:
                message = "Error: Unknown username or password"
                return render(request, 'register.html', {'message': message})

    return render(request,'register.html')

def esg_stat(request):
    reports = esg_reports.objects.all()
    total = len(reports)
    # Timeseries
    count_res = reports \
        .annotate(year=ExtractYear('edittime')) \
        .values('year').order_by('year').annotate(count=Count('id'))
    timedata = []
    for i in count_res:
        timedata.append("Year %(year)s : %(num)d reports" % {"year": i['year'], "num": i["count"] })
    # Source
    sourcedata = []
    sourcedata.append("Cninfo: %d reports" % len(esg_reports.objects.filter(site="cninfo")))
    sourcedata.append("SHSE: %d reports" % len(esg_reports.objects.filter(site="shse")))
    sourcedata.append("SZSE: %d reports" % len(esg_reports.objects.filter(site="szse")))
    # Pic
    return render(request, 'stat.html',{'total': total, 'timedata': timedata, 'sourcedata': sourcedata})