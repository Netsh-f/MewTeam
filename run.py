# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 17:10
# @Author  : Lynx
# @File    : run.py
#

import os
import platform

os.system("python manage.py makemigrations")
os.system("python manage.py migrate")

if platform.system() != "Linux":
  os.system("python manage.py runserver 8001")
# 本地环境，直接运行
else:
  os.system("python manage.py runserver 0.0.0.0:8001 & \n")
print("The backend is running!")
# 服务器环境，后台运行