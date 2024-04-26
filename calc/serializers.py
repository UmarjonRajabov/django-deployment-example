from rest_framework import serializers
from .models import KPI, KPIArchive, Employee
from django.conf import settings


class EmployeeSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    kpies = serializers.SerializerMethodField()

    def get_kpies(self, obj):
        kpi_queryset = obj.kpies.all()
        kpi_data = KPISerializer(kpi_queryset, many=True).data
        months = {}
        for kpi in kpi_data:
            month = kpi.pop('month')  # Remove 'month' from kpi data
            overall = kpi.pop('overall')  # Remove 'overall' from kpi data
            if month not in months:
                months[month] = {'month': month, 'overall': overall, 'month_data': []}
            months[month]['month_data'].append(kpi)
        return list(months.values())
        # if kpi_queryset.exists():  # Check if there are any KPI instances
        #     # Get the start date and overall value from the first KPI instance
        #     start_date = kpi_queryset.first().start
        #     overall_value = kpi_queryset.first().overall
        # else:
        #     start_date = None
        #     overall_value = None
        #
        #     # Serialize the KPI instances
        # month_data = KPISerializer(kpi_queryset, many=True).data
        # # Construct the response structure
        # return [{"month": start_date, "overall": overall_value, "month_data": month_data}]

        # month_data = KPISerializer(kpi_queryset, many=True).data
        # return [{"month": "2024-04-25", "overall": 0.24, "month_data": month_data}]

    def get_photo_url(self, obj):
        table_number = obj.table_number
        photo_filename = f"{table_number}.jpg"
        photo_url = settings.MEDIA_URL + 'employee_photos/' + photo_filename
        return photo_url

    # kpies = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("name", "photo_url", "table_number", "branch", "division", "department", "position",
                  "premium", "fixed", "kpies")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')  # Get the request object from serializer context
        if instance.photo:  # Check if photo field is not empty
            # Build absolute URL for photo using request object
            photo_url = request.build_absolute_uri(instance.photo.url)
            # Add photo_url to the response data
            data['photo_url'] = photo_url
        return data


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ("id","month", "performance_score", "kpi_name", "metric", "fact", "finished",
                  "definition", "method", "weight", "activity", "archived", "start", "end", "user",
                  "employee","overall")


#     # class Meta:
#     #     model = KPI
#     #     fields = '__all__'
#
#
# class EmployeeSerializer(serializers.ModelSerializer):
#     photo_url = serializers.SerializerMethodField()
#
#     kpies = serializers.SerializerMethodField()
#
#     def get_kpies(self, obj):
#         kpi_queryset = obj.kpi_set.all()
#         month_data = KPISerializer(kpi_queryset, many=True).data
#         return [{"month": month["month"], "overall": month["overall"], "month_data": month} for month in month_data]
#     def get_photo_url(self, obj):
#         table_number = obj.table_number
#         photo_filename = f"{table_number}.jpg"
#         photo_url = settings.MEDIA_URL + 'employee_photos/' + photo_filename
#         return photo_url
#
#     kpies = KPISerializer(many=True)
#
#     class Meta:
#         model = Employee
#         fields = ("name", "photo_url","table_number", "branch","division","department","position","premium","fixed", "kpies")
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         request = self.context.get('request')  # Get the request object from serializer context
#         if instance.photo:  # Check if photo field is not empty
#             # Build absolute URL for photo using request object
#             photo_url = request.build_absolute_uri(instance.photo.url)
#             # Add photo_url to the response data
#             data['photo_url'] = photo_url
#         return data


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
