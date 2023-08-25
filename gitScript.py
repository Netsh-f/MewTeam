# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 19:44
# @Author  : Lynx
# @File    : gitScript.py
#

import os
import subprocess

def check_merge_conflict(branch_name):
    merge_command = f"git merge {branch_name}"

    try:
        merge_output = subprocess.check_output(merge_command, stderr=subprocess.STDOUT, shell=True, text=True)
        if "CONFLICT" in merge_output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return True


branch_name = input("请输入个人开发分支名：")
confirmation = input("请确认位于个人开发分支并已将所有更改提交！[y/n]: ")

if confirmation.lower() == "y":
    os.system("git checkout dev")
    os.system("git pull")

    if check_merge_conflict(branch_name):
        print("检测到冲突，请修复后手动执行个人开发分支的同步操作！")
    else:
        os.system(f"git merge {branch_name}")
        os.system("git push")
        os.system(f"git checkout {branch_name}")
        os.system("git merge dev")
else:
    print("操作已取消。")