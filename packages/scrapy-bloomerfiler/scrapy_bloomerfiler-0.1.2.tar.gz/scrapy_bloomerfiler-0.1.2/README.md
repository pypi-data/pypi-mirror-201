### 处理若干个pdf水印事项
* 项目PYPI地址 https://pypi.org/project/scrapy_bloomerfiler/
* 安装:
```
pip install scrapy-bloomerfilter
```

* scrapy 管道中添加配置
```
ITEM_PIPELINES = {'scrapy_bloomerfiler.bloomerfilerpipeline': 400},
```

* `scrapy.cfg` 添加配置`REDIS_HOST / REDIS_PORT / REDIS_DB / REDIS_PASSWORD`
```
测试环境
[redis_cfg_dev]
REDIS_HOST = ***
REDIS_PORT = ***
REDIS_DB = ***
REDIS_PASSWORD= ***

正式环境
[redis_cfg_prod]
REDIS_HOST = ***
REDIS_PORT = ***
REDIS_DB = ***
REDIS_PASSWORD= ***
```

* scrapy settings 中添加
```
IF_PROD 是否为正式环境配置 eg : True
Data_Size 数据体量 eg: 1000*10000/百万级/千万级/千万 
Aim_Set  除重依据字段 Aim_Set <dict>  eg: {"title","all_json"}
```

* 环境变量中参数(可选)
```
IF_PROD 是否为正式环境配置 eg : True
```