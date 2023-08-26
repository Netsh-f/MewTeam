# ------- Litang Save The World! -------
#
# @Time    : 2023/8/26 10:24
# @Author  : Lynx
# @File    : forms.py
#

from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()