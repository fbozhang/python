from django.db import models


# Create your models here.
class Area(models.Model):
    """ 省市區 """
    name = models.CharField(max_length=20, verbose_name='名稱')
    # django會自動生成為parent_id
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上級行政區劃')
    # subs = [Area,Area,Area]
    #  related_name 关联的模型的名字
    # 默认是 关联模型类名小写_set     area_set
    # 我们可以通过 related_name 修改默认是名字，现在就改为了 subs

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市區'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
