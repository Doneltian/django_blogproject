from ..models import Post, Category
from django import template
from django.db.models.aggregates import Count
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


"""
这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，
并将函数 get_recent_posts 装饰为 register.simple_tag。
这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
注意 Django 1.9 后才支持 simple_tag 模板标签
"""


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


"""
这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
且是 Python 的 date 对象，精确到月份，降序排列。
接受的三个参数值表明了这些含义，一个是 created_time ，即 Post 的创建时间，month 是精度，
order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。例如我们写了 3 篇文章，
分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
"""


@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    # return Category.objects.all()
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
"""

"""
