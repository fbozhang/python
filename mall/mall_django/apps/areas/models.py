from django.db import models


# Create your models here.
class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True, verbose_name='上级行政区划')

    # subs = [Area,Area,Area]
    #  related_name 关联的模型的名字
    # 默认是 关联模型类名小写_set     area_set
    # 我们可以通过 related_name 修改默认是名字，现在就改为了 subs

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name


"""
省市区


id          name            parent_id

10000       河北省             NULL

10100       保定市             10000
10200       石家庄市            10000
10300       唐山市             10000


10101       雄县              10100
10102       安新县             10100



查询省份信息
 select * from tb_areas where parent_id is NULL;

 Area.objects.filter(parent=None)
 Area.objects.filter(parent__isnull=True)
 Area.objects.filter(parent_id__isnull=True)


查询市的信息
select * from tb_areas where parent_id=130000;

    Area.objects.filter(parent_id=130000)
    Area.objects.filter(parent=130000)

    >>> province=Area.objects.get(id=130000)  #省
    >>> province.subs.all()                   #市


查询区县的信息
select * from tb_areas where parent_id=130600;

    Area.objects.filter(parent_id=130600)
    Area.objects.filter(parent=130600)

    >>> city=Area.objects.get(id=130600)   #市
    >>> city.subs.all()                    #区县

"""