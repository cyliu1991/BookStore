from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from index.models import Book, PubName
import logging
from index.forms import TitleSearch
from django import forms
# Create your views here.


def update_book(request, book_id):
    # 用 book_id给每个书籍加上标记
    # 将其作为查找书籍的参数
    book_id = int(book_id)
    try:
        book = Book.objects.get(id=book_id)
    except Exception as e:
        return HttpResponse('--没有找到任何书籍---')
    if request.method == 'GET':
        return render(request, 'index/update_book.html', locals())
    elif request.method == 'POST':
        price = request.POST.get('price')
        retail_price = request.POST.get('retail_price')
        if not price or not retail_price:
            return HttpResponse('请输入更改后的零售价或市场价！')
        price = float(price)
        retail_price = float(retail_price)
        # 修改对象属性值
        book.price = price
        book.retail_price = retail_price
        # 存储更新后的状态
        book.save()
        # 重定向至127.0.0.1:8000/index/all_book/
        return HttpResponseRedirect('/index/all_book')
    return HttpResponse("书籍信息更新功能")


def book_not_list(request):
    return render(request, "index/book_not_list.html")


def search_title_form(request):
    return render(request, 'index/search_title.html', context={'form': TitleSearch()})


def search_title(request):
    form = TitleSearch(request.GET)
    if form.is_valid():
        books = Book.objects.filter(title__icontains=form.cleaned_data["title"])
        if not books:
            return HttpResponseRedirect("/index/book_not_list")
        return render(request, 'index/book_list.html', locals())
    else:
        return render(request, 'index/search_title.html', {'form': form})


def book_table(request):
    try:
        all_book = Book.objects.all().order_by('-price')
        if not all_book:
            return HttpResponse('书籍信息表为空，请录入！')
    except Exception as e:
        print(e)
    return render(request, "index/book_table.html", locals())


def add_book(request):
    if request.method == 'GET':
        return render(request, 'index/add_book.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        if not title:
            return HttpResponse("请给出一个正确的title")
        pub = request.POST.get('pub')
        price = float(request.POST.get('price', '999.99'))
        if not price:
            return HttpResponse('请输入价格')
        try:
            retail_price = float(request.POST.get('retail_price'))
            if not retail_price:
                return HttpResponse('请输入市场价')
        except Exception as e:
            print(e)

        old_book = Book.objects.filter(title=title)
        if old_book:
            return HttpResponse('你输入的书籍系统已经存在 !')
        try:
            pub1 = PubName.objects.get(pubname=str(pub))
            Book.objects.create(title=title, price=price, retail_price=retail_price, pub=pub1)
        except Exception as e:
            print('Add ErrorReason is %s' % (e))
        return HttpResponseRedirect('/index/all_book')
    return HttpResponse('请使用正确Http请求方法 !')



