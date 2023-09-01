"""
============================
# @Time    : 2023/9/1 13:11
# @Author  : Elaikona
# @FileName: regex_helper.py
===========================
"""
import re


def extract_user_ids(chat_content):
    pattern = r'<usertag>(\d+)<\/usertag>'
    matches = re.findall(pattern, chat_content)
    user_ids = [int(match) for match in matches]
    return user_ids
