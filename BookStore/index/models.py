from django.db import models


# Create your models here.
class PubName(models.Model):
    pubname = models.CharField('名称', max_length=255, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='书名')
    # public = models.CharField(max_length=50,verbose_name='出版社')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='定价')

    @property
    def default_price(self):
        return '￥30'

    retail_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='零售价', default=default_price)
    pub = models.ForeignKey(to=PubName, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "title: %s pub: %s price: %s" % (self.title, self.pub, self.price)


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    books = models.ManyToManyField(to="Book")

    def __str__(self):
        return "name: %s" % (self.name)


class UserInfo(models.Model):
    username = models.CharField(max_length=24, verbose_name='用户名')
    password = models.CharField(max_length=24, verbose_name='密码')


class ExtendUserInfo(models.Model):
    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    signature = models.CharField(max_length=255, verbose_name='用户签名', help_text='自建签名')
    nickname = models.CharField(max_length=255, verbose_name='昵称', help_text='自建昵称')