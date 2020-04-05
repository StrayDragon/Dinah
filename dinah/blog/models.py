from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "已删除"),
        (STATUS_NORMAL, "正常"),
    )
    name = models.CharField(max_length=50, verbose_name="名称",)
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS, verbose_name="状态",
    )
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "已删除"),
        (STATUS_NORMAL, "正常"),
    )
    name = models.CharField(max_length=10, verbose_name="名称",)
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS, verbose_name="状态",
    )
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS = (
        (STATUS_DELETE, "已删除"),
        (STATUS_NORMAL, "正常"),
        (STATUS_DRAFT, "草稿"),
    )
    title = models.CharField(max_length=255, verbose_name="标题",)
    desc = models.CharField(max_length=1024, verbose_name="简要",)
    content = models.TextField(verbose_name="正文", help_text="正文使用MarkDown语法标注")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS, verbose_name="状态",
    )
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        ordering = ["-id"]


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "已删除"),
        (STATUS_NORMAL, "正常"),
    )
    title = models.CharField(max_length=50, verbose_name="标题",)
    href = models.URLField(verbose_name="链接")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS, verbose_name="状态",
    )
    rank = models.PositiveIntegerField(
        default=1, choices=zip(range(1, 6), ""), verbose_name="权重", help_text="权重高的排名靠前"
    )
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS = (
        (STATUS_SHOW, "显示"),
        (STATUS_HIDE, "隐藏"),
    )
    SIDE_TYPES = (
        (1, "HTML"),
        (2, "最新文章"),
        (3, "最热文章"),
        (4, "最近评论"),
    )
    title = models.CharField(max_length=50, verbose_name="标题",)
    display_type = models.PositiveIntegerField(
        default=1, choices=SIDE_TYPES, verbose_name="展示类型",
    )
    content = models.CharField(
        max_length=500, blank=True, verbose_name="内容", help_text="若设置不为HTML, 可为空"
    )
    status = models.PositiveIntegerField(
        default=STATUS_SHOW, choices=STATUS, verbose_name="状态",
    )
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "已删除"),
        (STATUS_NORMAL, "正常"),
    )
    target = models.ForeignKey(Post, verbose_name="评论文章", on_delete=models.CASCADE)
    author = models.CharField(max_length=50, verbose_name="评论作者")
    content = models.CharField(max_length=2000, verbose_name="评论正文")
    home_site = models.URLField(verbose_name="主页")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS, verbose_name="状态",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"
