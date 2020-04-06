import dataclasses

from django.http import HttpResponse

from blog.models import Tag, Post, Category, SideBar
from utils.shortcuts import render_mako


def post_list_view(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        posts, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts, category = Post.get_by_category(category_id)
    else:
        posts = Post.latest_post()

    context = {
        "posts": posts,
        "category": category,
        "tag": tag,
        "sidebars": SideBar.get_all(),
    }
    context.update(dataclasses.asdict(Category.get_navs()))
    return render_mako(request, "blog/post_list.mako", context=context,)


def post_details_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {"post": post}
    context.update(dataclasses.asdict(Category.get_navs()))
    return render_mako(request, "blog/post_details.mako", context=context,)


def links_view(args):
    return HttpResponse("links")
