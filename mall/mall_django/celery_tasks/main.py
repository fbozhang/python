"""
生产者（任务，函数）
    @app.task
    def celery_send_sms_code(mobie,code):

        CCP().send_template_sms(mobie,[code,5],1)


    app.autodiscover_tasks(['celery_tasks.sms'])
消费者
    celery -A proj worker -l INFO

    在虚拟环境下执行指令
    celery -A celery实例的脚本路径 worker -l INFO

    本案例使用
    celery -A celery_tasks.main worker -l INFO

队列（中间人、经纪人）
    #2. 设置broker
    # 我们通过加载配置文件来设置broker
    app.config_from_object('celery_tasks.config')

    # 配置信息 key=value
    # 我们指定 redis为我们的broker(中间人，经纪人，队列)
    broker_url="redis://127.0.0.0:6379/15"

Celery -- 将这3者实现了。

    # 0. 为celery的运行 设置Django的环境
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')

    # 1. 创建celery实例
    from celery import Celery
    # 参数1： main 设置脚本路径就可以了。 脚本路径是唯一的
    app=Celery('celery_tasks')
"""
import os

# 設置django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_django.settings')

# 創建celery實例
from celery import Celery
# main設置脚本路徑
app = Celery(main='celery_tasks')

# 設置broker
# 通過加載配置文件來設置broker
app.config_from_object('celery_tasks.config')

# celery自動檢測指定包的任務
# autodiscover_tasks參數是列表
# 列表中的元素是tasks的路徑
app.autodiscover_tasks(['celery_tasks.sms'])