from rest_framework import serializers
from .models import KPI, KPIArchive


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'




class KPIArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIArchive
        fields = '__all__'
