import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import UserInfo


def login_view(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return HttpResponseRedirect('index/allbook')
        if 'username' in request.COOKIES:
            request.session['username'] = request.COOKISE['username']
            return HttpResponseRedirect('index/allbook')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        if not username or not password:
            error = '你输入的用户名或者密码错误！'
            return render(request, 'user/login.html', locals())
        users = UserInfo.objects.filter(username=username, password=password)
        if not users:
            error = '用户不存在或用户密码输入错误!!'
            return render(request, 'user/login.html', locals())
            # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
        users = users[0]
        request.session['username'] = username
        response = HttpResponseRedirect('/index/allbook')
        # 检查post 提交的所有键中是否存在 isSaved 键
        if 'isSaved' in request.POST.keys():
            # 若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
            response.set_cookie('username', username, 60 * 60 * 24 * 7)
        return response