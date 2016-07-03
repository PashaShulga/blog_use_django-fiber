import json

from django.core import urlresolvers
# from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.encoding import force_text

from fiber.models import Page, ContentItem, PageContentItem
from test_util import format_list, condense_html_whitespace


class ContentItemTest(object):

    def generate_data(self):
        """
        Generate test data:
         - page1, page2, page3
         - content a: on page 1 and 2
         - content b: on page 3
         - content c: unused
        """
        page1 = Page.objects.create(title='page1')
        page2 = Page.objects.create(title='page2')
        page3 = Page.objects.create(title='page2')

        content_a = ContentItem.objects.create(name='a')
        content_b = ContentItem.objects.create(name='b')
        content_c = ContentItem.objects.create(name='c')

        PageContentItem.objects.create(page=page1, content_item=content_a)
        PageContentItem.objects.create(page=page2, content_item=content_a)
        PageContentItem.objects.create(page=page3, content_item=content_b)


class PageTest(object):

    def generate_data(self):
        """
        ---home
        ------section1 (/section1/)
        ---------abc (/section1/abc/)
        ------------xyz (/section1/abc/xyz/)
        ------section2 (/section2/)
        ---------def (/def/)  # absolute url
        ---------ghi (/section2/ghi/)
        """
        page_home_id = Page.objects.create(title='home').id
        page_section1_id = Page.objects.create(title='section1', parent_id=page_home_id, url='section1').id
        page_section2_id = Page.objects.create(title='section2', parent_id=page_home_id, url='section2').id
        page_abc_id = Page.objects.create(title='abc', parent_id=page_section1_id, url='abc').id
        Page.objects.create(title='xyz', parent_id=page_abc_id, url='xyz')
        page_def_id = Page.objects.create(title='def', parent_id=page_section2_id, url='/def/').id  # absolute url
        page_ghi_id = Page.objects.create(title='ghi', parent_id=page_section2_id, url='ghi').id
        Page.objects.create(title='example', url='http://example.com')

        page_def = Page.objects.get(id=page_def_id)
        page_ghi = Page.objects.get(id=page_ghi_id)
        page_ghi.move_to(page_def, 'right')

    def test_move_page(self):
        # generate data
        self.generate_data()

        ContentItem.objects.create(
            name='a',
            content_markup='"abc":/section1/abc/',
            content_html='<p><a href="/section1/abc/">abc</a></p>'
        )
        ContentItem.objects.create(
            name='b',
            content_markup='"xyz":/section1/abc/xyz/',
            content_html='<p><a href="/section1/abc/xyz/">xyz</a></p>'
        )