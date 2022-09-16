from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.models import ContentCategory
from utils.goods import get_categories


class IndexView(View):

    def get(self, request):
        # 商品分類數據
        categories = get_categories()

        # 廣告數據
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request, 'index.html', context=context)
