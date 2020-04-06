import dataclasses
from typing import List, Optional, Dict, Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.template.loader import render_to_string

from utils.shortcuts import render_mako_to_string

DISPLAY_COMMENT = 4

DISPLAY_HOT = 3

DISPLAY_LATEST = 2

DISPLAY_HTML = 1


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "删除"),
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

    def __str__(self):
        return self.name

    @dataclasses.dataclass
    class NavsInfo:
        navs: List["Category"]
        categories: List["Category"]

    @staticmethod
    def get_navs() -> NavsInfo:
        categories: QuerySet = Category.objects.filter(status=Category.STATUS_NORMAL)
        # nav_categories = categories.filter(is_nav=True)
        # normal_categories = categories.filter(is_nav=False)
        nav_categories: List[Category] = []
        normal_categories: List[Category] = []
        for c in categories:
            if c.is_nav:
                nav_categories.append(c)
            else:
                normal_categories.append(c)
        return Category.NavsInfo(navs=nav_categories, categories=normal_categories,)


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "删除"),
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

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS = (
        (STATUS_DELETE, "删除"),
        (STATUS_NORMAL, "正常"),
        (STATUS_DRAFT, "草稿"),
    )
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
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
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    @staticmethod
    def hot_posts() -> QuerySet:
        return Post.objects.filter(status=Post.STATUS_NORMAL).order_by("-pv")

    @staticmethod
    def get_by_tag(tag_id: int) -> (List["Post"], Optional[Tag]):
        tag = None
        posts = []
        if tag_id:
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                pass
            else:
                posts = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related(
                    "owner", "category"
                )
        return posts, tag

    @staticmethod
    def get_by_category(category_id) -> (List["Post"], Optional[Category]):
        category = None
        posts = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
            else:
                posts = posts.filter(category_id=category_id)
        return posts, category

    @staticmethod
    def latest_post() -> QuerySet:
        qs: QuerySet = Post.objects.filter(status=Post.STATUS_NORMAL)
        return qs


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "删除"),
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

    def __str__(self):
        return self.title


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS = (
        (STATUS_SHOW, "显示"),
        (STATUS_HIDE, "隐藏"),
    )
    SIDE_TYPES = (
        (DISPLAY_HTML, "HTML"),
        (DISPLAY_LATEST, "最新文章"),
        (DISPLAY_HOT, "最热文章"),
        (DISPLAY_COMMENT, "最近评论"),
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

    def __str__(self):
        return self.title

    @staticmethod
    def get_all() -> QuerySet:
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    @property
    def content_html(self) -> str:
        result = ""
        if self.display_type == DISPLAY_HTML:
            result = self.content
        elif self.display_type == DISPLAY_LATEST:
            ctx = {"posts": Post.latest_post()}
            result = render_mako_to_string("blocks/sidebar_posts.mako", context=ctx)
        elif self.display_type == DISPLAY_HOT:
            ctx = {"posts": Post.hot_posts()}
            result = render_mako_to_string("blocks/sidebar_posts.mako", context=ctx)
        elif self.display_type == DISPLAY_HOT:
            ctx = {"comments": Comment.objects.filter(status=Comment.STATUS_NORMAL)}
            result = render_mako_to_string("blocks/sidebar_comments.mako", context=ctx)
        return result


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS = (
        (STATUS_DELETE, "删除"),
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
        verbose_name = verbose_name_plural = "评论"
