from django.http import HttpResponse
from django.shortcuts import render
from index.models import Book
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


