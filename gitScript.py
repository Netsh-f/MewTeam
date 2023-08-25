# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 19:44
# @Author  : Lynx
# @File    : gitScript.py
#

import os

branch_name = input("请输入个人开发分支名：")
confirmation = input("请确认位于个人开发分支并已将所有更改提交！[y/n]: ")

if confirmation.lower() == "y":
    os.system("git checkout dev")
    os.system("git pull")
    os.system(f"git merge {branch_name}")
    os.system("git push")
    os.system(f"git checkout {branch_name}")
    os.system("git merge dev")
else:
    print("操作已取消。")