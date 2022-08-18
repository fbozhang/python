from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)  # 总长10小数2

    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to， 与哪张表关联
    #   - to_field， 表中的哪一列关联
    # depart = models.ForeignKey(to="Department", to_field="id")
    # 2.Django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Prettynum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空:  null=True, blank=True
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (1, '已占用'),
        (2, '未占用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)
