from django.db import models

# Create your models here.
from django.db import models
from django.utils.six import python_2_unicode_compatible


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

    """
    这里我们会保存评论用户的 name（名字）、email（邮箱）、url（个人网站），
    用户发表的内容将存放在 text 字段里，created_time 记录评论时间。
    最后，这个评论是关联到某篇文章（Post）的，由于一个评论只能属于一篇文章，一篇文章可以有多个评论，是一对多的关系，因此这里我们使用了 ForeignKey。
    关于 ForeKey 我们前面已有介绍，这里不再赘述。
    同时注意我们为 DateTimeField 传递了一个 auto_now_add=True 的参数值。
    auto_now_add 的作用是，当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间。
    created_time 记录用户发表评论的时间，我们肯定不希望用户在发表评论时还得自己手动填写评论发表时间，这个时间应该自动生成。
    """
