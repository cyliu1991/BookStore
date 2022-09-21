from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from index.models import Book, PubName
import logging
from django import forms
# Create your views here.


def search_title_form(request):
    return render(request, 'index/search_title.html')


def search_title(request):
    if not request.GET.get('title', ''):
        errors = ['输入的书名是无效']
        return render(request, 'index/search_title.html', locals())
    logging.basicConfig(level=logging.DEBUG)
    # 查询title忽略大小写,所得类型为QuerySet
    title = Book.objects.filter(title__icontains=request.GET['title'])
    logging.debug("title:%s", title)
    name = ""
    pub = ""
    price = ""
    if title.exists():
        name = title[0].title
        pub = title[0].pub
        price = title[0].price
        logging.debug("name:%s", name)
    return render(request, 'index/book_list.html', {"name": name, "pub": pub, "price": price})


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


