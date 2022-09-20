from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from apps.contents.models import ContentCategory
from utils.goods import *
from apps.goods.models import *


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


class ListView(View):

    def get(self, request, category_id):
        # 接收參數
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')
        # 獲取分類id

        # 根據分類id進行分類數據的查詢驗證
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '參數缺失'})

        # 獲取麵包屑數據
        breadcrumb = get_breadcrumb(category)

        # 查詢分類對應的sku數據，然後排序，然後分頁
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        # 分頁
        from django.core.paginator import Paginator
        #  object_list 列表數據, per_page 每頁多少條數據
        paginator = Paginator(object_list=skus, per_page=page_size)

        # 獲取指定頁碼的數據
        page_skus = paginator.page(page)

        sku_list = []
        # 將對象轉換為列表數據
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 獲取縂頁碼
        total_num = paginator.num_pages

        # 返回相應
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': sku_list,
            'count': total_num
        })


class HotView(View):

    def get(self, request, category_id):
        # 根據分類id進行分類數據的查詢驗證
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '參數缺失'})

        # 查詢分類對應的sku數據，然後排序，然後分頁
        skus = SKU.objects.filter(category=category, is_launched=True).order_by('-sales')

        hot_skus_list = []
        # 將對象轉換為列表數據, 顯示銷量前三為熱銷
        top = 3
        for sku in skus:
            if top == 0:
                break
            hot_skus_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })
            top -= 1

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'hot_skus': hot_skus_list})


""" 借助haystack來對接elasticsearch """
from haystack.views import SearchView


class SKUSearchView(SearchView):

    def create_response(self):
        """ 重寫 create_response 方法"""

        # 獲取搜索的結果
        context = self.get_context()

        sku_list = []
        for sku in context['page'].object_list:
            sku_list.append({
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })

        return JsonResponse(sku_list, safe=False)


class DetailView(View):
    """ 詳情頁 """

    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            pass
        # 分類數據
        categories = get_categories()
        # 麵包屑
        breadcrumb = get_breadcrumb(sku.category)
        # SKU信息

        # 規格信息
        goods_spece = get_goods_specs(sku)

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_spece,
        }

        return render(request, 'detail.html', context=context)


from datetime import date


class CategoryVistCountView(View):

    def post(self, request, category_id):
        # 驗證參數
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '沒有此分類'})

        # 查詢當天 這個分類的記錄有沒有
        today = date.today()

        try:
            gvc = GoodsVisitCount.objects.get(category=category, date=today)
        except GoodsVisitCount.DoesNotExist:
            # 沒有 新建數據
            GoodsVisitCount.objects.create(category=category, date=today, count=1)
        else:
            # 有 更新數據
            gvc.count += 1
            gvc.save()

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
