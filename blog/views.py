from django.shortcuts import render

# Create your views here.
import markdown
from  django.http import HttpResponse
from .models import Post
from django.shortcuts import render, get_object_or_404
# 引入 Category 类
from .models import Post, Category
from comments.forms import CommentForm

def index(request):
    # return1 HttpResponse("欢迎访问我的博客首页!")
    """return2 render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })"""

    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index3.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 记得在顶部引入 markdown 模块
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    # return render(request, 'blog/detail.html', context={'post': post})
    return render(request, 'blog/detail.html', context=context)


"""return1的解释
这个两行的函数体现了这个过程。它首先接受了一个名为 request 的参数，
这个 request 就是 Django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例。
然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是 Django 帮我们封装好的，
它是类 HttpResponse 的一个实例，只是我们给它传了一个自定义的字符串参数。
浏览器接收到这个响应后就会在页面上显示出我们传递的内容 ：欢迎访问我的博客首页！
"""

"""return2的解释
这里我们不再是直接把字符串传给 HttpResponse 了，而是调用 Django 提供的 render 函数。
这个函数根据我们传入的参数来构造 HttpResponse。
我们首先把 HTTP 请求传了进去，然后 render 根据第二个参数的值 blog/index.html 找到这个模板文件并读取模板中的内容。
之后 render 根据我们传入的 context 参数的值把模板中的变量替换为我们传递的变量的值，{{ title }} 被替换成了 context 字典中 title 
对应的值，同理 {{ welcome }} 也被替换成相应的值。
最终，我们的 HTML 模板中的内容字符串被传递给 HttpResponse 对象并返回给浏览器（Django 
在 render 函数里隐式地帮我们完成了这个过程），这样用户的浏览器上便显示出了我们写的 HTML 模板的内容
"""

"""
我们曾经在前面的章节讲解过模型管理器 objects 的使用。
这里我们使用 all() 方法从数据库里获取了全部的文章，存在了 post_list 变量里。
all 方法返回的是一个 QuerySet（可以理解成一个类似于列表的数据结构），由于通常来说博客文章列表是按文章发表时间倒序排列的，
即最新的文章排在最前面，所以我们紧接着调用了 order_by 方法对这个返回的 queryset 进行排序。
排序依据的字段是 created_time，即文章的创建时间。- 号表示逆序，如果不加 - 则是正序。 
接着如之前所做，我们渲染了 blog\index.html 模板文件，并且把包含文章列表数据的 post_list 变量传给了模板。
"""

"""
视图函数很简单，它根据我们从 URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章 id 为该值的记录，
然后传递给模板。注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
"""


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index3.html', context={'post_list': post_list})


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index3.html', context={'post_list': post_list})

"""
这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。
get_object_or_404 函数和 detail 视图中一样，其作用是如果用户访问的分类不存在，则返回一个 404 错误页面以提示用户访问的资源不存在。
然后我们通过 filter 函数过滤出了该分类下的全部文章。同样也和首页视图中一样对返回的文章列表进行了排序。
"""