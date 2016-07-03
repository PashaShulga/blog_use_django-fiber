from django.views.generic import DetailView, ListView, View
from fiber.models import Page, ContentItem, PageContentItem
from django.shortcuts import HttpResponse, get_list_or_404, get_object_or_404, render_to_response
from django.template import loader
from fiber.views import FiberPageMixin
from django.core.urlresolvers import reverse
from fiber.views import FiberTemplateView
import json


class ViewBlog(FiberTemplateView):

    def get(self, request, *args, **kwargs):
        blog_items = get_list_or_404(Page, parent_id=Page.objects.get(url='blog'))
        data = {"blog_list": blog_items}
        return render_to_response('test_blog.html', context=data)


class ViewBlogItem(FiberTemplateView):

    def get(self, request, *args, **kwargs):
        blog_item = get_list_or_404(Page, url=kwargs['page_slug'])
        page_id = blog_item[0].id
        content_item = get_list_or_404(ContentItem, id=get_object_or_404(PageContentItem, page_id=page_id).content_item_id)
        data = {"blog_list": blog_item,
                "content_item": content_item}
        return render_to_response('tpl-blog-item.html', context=data)