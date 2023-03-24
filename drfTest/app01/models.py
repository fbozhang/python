from django.db import models


# Create your models here.
class Author(models.Model):
    """ 作者表 """
    author = models.CharField(verbose_name="作者", max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=64)
    direction = models.CharField(verbose_name='方向', max_length=512)
    useNum = models.IntegerField(verbose_name='文章引用次数')
    company_name = models.CharField(verbose_name='單位名稱', max_length=256, default='')
    documentTitle = models.CharField(verbose_name="標題", max_length=512, default='')

    choices_yn = (
        (1, '是'),
        (2, '否'),
    )
    isCorrespondingAuthor = models.SmallIntegerField(verbose_name='是通讯作者', choices=choices_yn, default=2)
    isOnlyAuthor = models.SmallIntegerField(verbose_name='是唯一作者', choices=choices_yn, default=2)

    def __str__(self):
        return self.author


class Area(models.Model):
    """ 國家分區 """
    area = models.CharField(verbose_name='國家分區', max_length=32)

    def __str__(self):
        return self.area


class Country(models.Model):
    """ 国家表 """
    country = models.CharField(verbose_name="国家", max_length=32)
    area = models.ForeignKey(to='Area', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.country


class Detail(models.Model):
    """ 详情表 """
    author = models.ForeignKey(to="Author", to_field="id", on_delete=models.CASCADE)
    h_index = models.IntegerField(verbose_name="h_index")
    company = models.CharField(verbose_name="归属机构", max_length=256)
    city = models.CharField(verbose_name="城市", max_length=256)
    country = models.ForeignKey(to="Country", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    documentTitle = models.CharField(verbose_name="参考文献", max_length=512)
