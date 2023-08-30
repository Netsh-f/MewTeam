from rest_framework import serializers

from project.models import Project, Prototype, Document, DocumentContent, DocumentDir, PrototypeContent


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class CustomParDirField(serializers.StringRelatedField):
    def to_representation(self, value):
        if value.par_dir is None:  # 根据你的条件判断
            return "root"
        return value.name

class DocumentSerializer(serializers.ModelSerializer):
    par_dir = CustomParDirField()
    class Meta:
        model = Document
        fields = '__all__'

class DocumentContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentContent
        fields = '__all__'


class DocumentContentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentContent
        exclude = ['content']


class PrototypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prototype
        fields = "__all__"

class PrototypeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrototypeContent
        fields = "__all__"