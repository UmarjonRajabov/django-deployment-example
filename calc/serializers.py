from rest_framework import serializers
from .models import KPI, KPIArchive, Employee
from django.conf import settings


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        table_number = obj.table_number
        photo_filename = f"{table_number}.jpg"
        photo_url = settings.MEDIA_URL + 'employee_photos/' + photo_filename
        return photo_url

    kpies = KPISerializer(many=True)

    class Meta:
        model = Employee
        fields = ("name", "photo", "photo_url", "kpies")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')  # Get the request object from serializer context
        if instance.photo:  # Check if photo field is not empty
            # Build absolute URL for photo using request object
            photo_url = request.build_absolute_uri(instance.photo.url)
            # Add photo_url to the response data
            data['photo_url'] = photo_url
        return data


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
        fields = ['id', 'month', 'performance_score', 'kpi_name', 'metric', 'fact', 'finished', 'premium', 'definition',
                  'method', 'weight', 'activity', 'overall', 'start', 'end', 'user', 'employee']
