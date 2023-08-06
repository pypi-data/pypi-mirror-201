from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

class SuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()