# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 19:44
# @Author  : Lynx
# @File    : gitScript.py
#

import os

branch_name = input("请输入个人开发分支名[ (a)lynx / (b)Elaikona-feature ]：")
confirmation = input("请确认位于个人开发分支并已将所有更改提交！[y/n]: ")

if branch_name.lower() == 'a':
    branch_name = 'lynx'
elif branch_name.lower() == 'b':
    branch_name = 'Elaikona-feature'

if confirmation.lower() == "y":
    os.system("git checkout dev")
    os.system("git pull")
    os.system(f"git checkout {branch_name}")
    os.system("git merge dev")
    print("该步骤可能会发生冲突，git分析中……")
    os.system("git checkout dev")
    os.system(f"git merge {branch_name}")
    os.system("git push")
    os.system(f"git checkout {branch_name}")
else:
    print("操作已取消。")