"""
============================
# @Time    : 2023/8/26 16:39
# @Author  : Elaikona
# @FileName: serializer.py
===========================
"""
from rest_framework import serializers

from project.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class DocumentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['content']
