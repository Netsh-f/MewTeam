from rest_framework import serializers

from project.models import Project, Prototype, Document, DocumentContent, DocumentDir


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class DocumentDirSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDir
        fields = ['name']

    # def to_representation(self, instance):
class DocumentSerializer(serializers.ModelSerializer):
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
