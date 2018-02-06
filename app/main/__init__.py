from flask import Blueprint

# 通过实例化 Flask 提供的 Blueprint 类对象，就可以创建蓝本（这里 main 即为 Blueprint 的实例）
# Blueprint() 有两个必须的参数：第一个为蓝本的名字(即'main')，第二个为蓝本所在的包或者模块，一般使用__name__即可
main = Blueprint('main', __name__)

# main蓝本的 视图处理函数都保存在当前文件夹(from .)下的views.py文件里面(import views)
# 这里进行导入操作是为了将路由与蓝本关联起来（即让程序识别哪些路由由main蓝本进行管理）
# 在文件末尾导入，是为了避免循环导入依赖，因为在 views.py 中要导入蓝本main
from . import views