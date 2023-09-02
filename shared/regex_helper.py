"""
============================
# @Time    : 2023/9/1 13:11
# @Author  : Elaikona
# @FileName: regex_helper.py
===========================
"""
import re

from user.models import User


def extract_user_ids(chat_content):
    pattern = r'<usertag>(\d+)<\/usertag>'
    matches = re.findall(pattern, chat_content)
    modified_content = chat_content
    user_ids = []
    for match in matches:
        user_id = int(match.group(1))
        username = User.objects.get(id=user_id).name
        modified_content = modified_content.replace(match.group(0), "@" + username)
        user_ids.append(int(match))
    return user_ids, modified_content
