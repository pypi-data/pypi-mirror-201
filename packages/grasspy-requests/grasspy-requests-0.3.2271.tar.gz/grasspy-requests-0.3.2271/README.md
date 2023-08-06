# 网络请求 (requests)

#### 介绍
优雅简单的 python requests 库的草蟒中文版

#### 安装方法

`python -m pip install -U grasspy-requests`

#### 使用简介

```python
GET 基本使用:

   >>> 导入 网络请求
   >>> 响应 = 网络请求.查_get('https://www.grasspy.cn')
   >>> 响应.状态码
   200
   >>> '中文编程' 在 响应.内容.解码('utf-8')
   True

... 或 POST:

   >>> 数据 = 字典型(key1='value1', 键2='值2')
   >>> 响应 = 网络请求.增_post('https://httpbin.org/post', 数据=数据)
   >>> 打印(响应.文本)
   {
     ...
     "form": {
       "key1": "value1",
       "\u952e2": "\u503c2"
     },
     ...
   }

当然也支持其他 HTTP 方法.
```
