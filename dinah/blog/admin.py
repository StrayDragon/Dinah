from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag, Comment, Link, SideBar


class BaseOwnerAdmin(admin.ModelAdmin):
    exclude = ("owner",)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)
        return qs.filter(owner=request.user)


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset: QuerySet):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "is_nav", "created_time", "post_count")
    fields = ("name", "status", "is_nav")

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")

    fields = ("name", "status")


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        "title",
        "category",
        "status",
        "created_time",
        "operator",
    ]
    list_display_links = ()
    # list_filter = ["category"]

    list_filter = [CategoryOwnerFilter]

    search_fields = ["title", "category__name"]
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    fields = [
        ("category", "title"),
        "desc",
        "status",
        "content",
        "tag",
    ]

    def operator(self, obj):
        return format_html(
            """<a href="{}">编辑</a>""", reverse("admin:blog_post_change", args=(obj.id,))
        )

    operator.short_description = "操作"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("target", "author", "content", "home_site", "created_time")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "href", "status", "rank", "created_time")
    fields = ("title", "href", "status", "rank")

    def save_model(self, request, obj, form, change):
        obj.owner = request.owner
        return super().save_model(request, obj, form, change)


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ("title", "display_type", "content", "created_time")
    fields = ("title", "display_type", "content")

    def save_model(self, request, obj, form, change):
        obj.owner = request.owner
        return super().save_model(request, obj, form, change)


@admin.register(LogEntry,)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["object_repr", "object_id", "action_flag", "user", "change_message"]
