# -*- coding:utf-8 -*-
# @Time : 2023/3/24 23:55
# @Author: fbz
# @File : serializers.py
from rest_framework import serializers
from app01.models import Author


# 反序列化验证顺序: 字段类型 -> 字段选项 -> 单个字段(validate_字段名) -> 多个字段(validate)
class AutherSerializers(serializers.Serializer):
    # 变量名与模型字段名一样
    # 类型与模型类型一样
    # read_only 只用于序列化使用，反序列化的时候 忽略该字段
    id = serializers.IntegerField(read_only=True)
    # 通过字段选项验证数据。例如：max_length=10, min_length=2
    author = serializers.CharField(max_length=10, min_length=2)
    # required 表明该字段在反序列化时必须输入，默认True
    email = serializers.CharField(required=False)
    # write_only 只用于反序列化使用，序列化的时候 忽略该字段
    direction = serializers.CharField(write_only=True)
    useNum = serializers.IntegerField(max_value=5)
    company_name = serializers.CharField()
    documentTitle = serializers.CharField()

    # 如果有单个字段验证先验证单个字段再验证多个字段
    # 单个字段验证 validate_字段名
    def validate_company_name(self, attrs):
        # 写额外的检测代码
        if len(attrs) < 3:
            raise serializers.ValidationError('单位名称不能小于3')

        return attrs

    # 多个字段验证
    def validate(self, data):
        company_name = data.get('company_name')
        documentTitle = data.get('documentTitle')

        if len(company_name) < 3 or len(documentTitle) < 3:
            raise serializers.ValidationError('单位名称和标题不能小于3')

        return data

    # 如果序列化器是继承 Serializers
    # 当调用序列化器的save方法时，会触发调用 序列化器的create方法
    def create(self, validated_data):
        # validated_data 没有问题的数据

        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance       序列化器创建时 传递的对象
        # validated_data 没有问题的数据

        # get(key,default_value), 如果key是None，则使用默认值
        instance.author = validated_data.get('author', instance.author)
        instance.direction = validated_data.get('direction', instance.direction)
        instance.useNum = validated_data.get('useNum', instance.useNum)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.documentTitle = validated_data.get('documentTitle', instance.documentTitle)
        instance.save()  # 调用保存方法数据才会入库

        return instance


class AreaSerializers(serializers.Serializer):
    area = serializers.CharField()


class CountrySerializers(serializers.Serializer):
    country = serializers.CharField()

    # 对外键的学习
    # area = serializers.IntegerField()
    # TypeError: int() argument must be a string, a bytes-like object or a number, not 'Area'

    # 方法1
    # 如果定义的序列化起外键字段类型为 IntegerField
    # 那么定义的序列化器字段名 必须和数据库中的外键字段名一致
    # area_id = serializers.IntegerField()

    # 方法2
    # 如果想要外键数据的key就是模型字段名字，那么PrimaryKeyRelatedField 就可以获取到关联的模型id
    # queryset 再验证数据的时候告诉系统在哪匹配外键数据
    # AssertionError: Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only=`True`.
    # from app01.models import Area
    # area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    # 或者 read_only=True,意思是不验证了
    # area = serializers.PrimaryKeyRelatedField(read_only=True)

    # 方法3
    # 如果想要获取外键字段关联的 字符串信息，可以使用 StringRelatedField
    # 实际上获取的是模型中 def __str__(self): 的返回值
    # area = serializers.StringRelatedField()

    # 方法4
    area = AreaSerializers()

    # 方法5 在下面的 AreaCountrySerializers


class AreaCountrySerializers(serializers.Serializer):
    area = serializers.CharField()
    country_set = CountrySerializers(many=True)


from app01.models import Country, Area


class CountryModelSerializers(serializers.ModelSerializer):
    # country = serializers.CharField(min_length=1)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country  # ModelSerializer 必须设置 model
        fields = '__all__'  # 设置自动生成的字段列表 __all__ 表示所有
        # fields = ['id', 'country']
        # exclude = ['id']  # 出去列表中的字段，其他字段都生成

        # 只读字段列表
        # read_only_fields = ['country']

        extra_kwargs = {
            # '字段名': {'选项名':value}
            'country': {
                'min_length': 1,
                'max_length': 10,
            }
        }


class AreaModelSerializers(serializers.ModelSerializer):
    country = CountryModelSerializers(many=True, required=True)

    class Meta:
        model = Area
        fields = '__all__'

    # 序列化器嵌套序列化器写入数据的时候默认不写入多方实体的模型数据(本来应该报错，但是好像不报错了就是存不了数据库而已)
    # 需要自己实现create方法来实现数据的写入
    # 写入数据的思想：因为当前 地区和国家的关系是 1对多 应该想写入1的模型数据，再写入 多的模型数据
    def create(self, validated_data):
        # 先把validated_data 的嵌套数据分解开
        country = validated_data.pop('country')

        # 先写入 1 的模型数据
        area = Area.objects.create(**validated_data)

        # 再写入 多 的模型数据
        for item in country:
            Country.objects.create(area=area, **item)

        return area
