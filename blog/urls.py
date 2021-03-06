from django.conf.urls import  url
from  . import views
app_name = 'blog'
urlpatterns =[
    # url(r'^123',views.index,name='index'),
    url(r'^123',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.Archives.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]

"""
绑定关系的写法是把网址和对应的处理函数作为参数传给 url 函数（第一个参数是网址，第二个参数是处理函数），
另外我们还传递了另外一个参数 name，这个参数的值将作为处理函数 index 的别名，这在以后会用到。
注意这里我们的网址是用正则表达式写的，Django 会用这个正则表达式去匹配用户实际输入的网址，
如果匹配成功，就会调用其后面的视图函数做相应的处理。


比如说我们本地开发服务器的域名是 http://127.0.0.1:8000，
那么当用户输入网址 http://127.0.0.1:8000 后，
Django 首先会把协议 http、域名 127.0.0.1 和端口号 8000 去掉，
此时只剩下一个空字符串，
而 r'^$' 的模式正是匹配一个空字符串（这个正则表达式的意思是以空字符串开头且以空字符串结尾），
于是二者匹配，Django 便会调用其对应的 views.index 函数。

注意：在项目根目录的 blogproject\ 目录下（即 settings.py 所在的目录），
原本就有一个 urls.py 文件，这是整个工程项目的 URL 配置文件。
而我们这里新建了一个 urls.py 文件，且位于 blog 应用下。
这个文件将用于 blog 应用相关的 URL 配置。不要把两个文件搞混了。
"""


"""
首页视图匹配的 URL 去掉域名后其实就是一个空的字符串。
对文章详情视图而言，每篇文章对应着不同的 URL。
比如我们可以把文章详情页面对应的视图设计成这个样子：
当用户访问 <网站域名>/post/1/ 时，显示的是第一篇文章的内容，
而当用户访问 <网站域名>/post/2/ 时，显示的是第二篇文章的内容，
这里数字代表了第几篇文章，也就是数据库中 Post 记录的 id 值。


Django 使用正则表达式来匹配用户访问的网址。
这里 r'^post/(?P<pk>[0-9]+)/$' 整个正则表达式刚好匹配我们上面定义的 URL 规则。
这条正则表达式的含义是，以 post/ 开头，后跟一个至少一位数的数字，并且以 / 符号结尾，如 post/1/、 post/255/ 等都是符合规则的，
[0-9]+ 表示一位或者多位数。此外这里 (?P<pk>[0-9]+) 表示命名捕获组，
其作用是从用户访问的 URL 里把括号内匹配的字符串捕获并作为关键字参数传给其对应的视图函数 detail。
比如当用户访问 post/255/ 时（注意 Django 并不关心域名，而只关心去掉域名后的相对 URL），
被括起来的部分 (?P<pk>[0-9]+) 匹配 255，那么这个 255 会在调用视图函数 detail 时被传递进去，
实际上视图函数的调用就是这个样子：detail(request, pk=255)。
我们这里必须从 URL 里捕获文章的 id，因为只有这样我们才能知道用户访问的究竟是哪篇文章。
"""

"""
此外我们通过 app_name='blog' 告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
我们看到 blog\ urls.py 目前有两个视图函数，并且通过 name 属性给这些视图函数取了个别名，分别是 index、detail。
但是一个复杂的 Django 项目可能不止这些视图函数，例如一些第三方应用中也可能有叫 index、detail 的视图函数，那么怎么把它们区分开来，防止冲突呢？
方法就是通过 app_name 来指定命名空间，命名空间具体如何使用将在下面介绍。如果你忘了在 blog\ urls.py 中添加这一句，接下来你可能会得到一个 NoMatchReversed 异常。
"""