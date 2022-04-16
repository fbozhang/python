# -*- coding:utf-8 -*-
# @Time : 2022/4/11 22:34
# @Author: fbz
# @File : visualization.py


from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd

df = pd.read_csv('data.csv',encoding='utf-8')
# print(df)

china_map = (
    Map()
    .add('現有確診',[list(i) for i in zip(df['area'].values.tolist(),df['curConfirm'].values.tolist())])
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各地區確診人數'),
        visualmap_opts=opts.VisualMapOpts(max_=200,is_inverse=True)
    )
)
china_map.render('demo.html')