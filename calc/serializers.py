from rest_framework import serializers
from .models import KPI, KPIArchive


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'


# class KPIArchiveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KPIArchive
#         fields = '__all__'


class KPIArchiveSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.month.strftime('%Y-%m') if obj.month else None

    class Meta:
        model = KPIArchive
        fields = ['id', 'month', 'performance_score', 'kpi_name', 'metric', 'fact', 'finished', 'premium', 'definition', 'method', 'weight', 'activity', 'overall', 'start', 'end', 'user', 'employee']
