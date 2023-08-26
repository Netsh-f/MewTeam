from rest_framework import serializers

from project.models import Project, Prototype, Document


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class DocumentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['content']


class PrototypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prototype
        fields = "__all__"
