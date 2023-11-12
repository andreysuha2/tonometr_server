from diary.models import Record as DiaryRecord
from rest_framework import serializers

class PressureFieldSerializer(serializers.Serializer):
    high = serializers.IntegerField(required=True, min_value=10, max_value=999)
    lower = serializers.IntegerField(required=True, min_value=10, max_value=999)

class DiaryRecordSerializer(serializers.HyperlinkedModelSerializer):
    pulse = serializers.IntegerField(required=True, min_value=10, max_value=999)
    timestamp = serializers.DateTimeField(required=True)
    
    class Meta:
        model = DiaryRecord
        fields = ('pulse', 'timestamp', 'pressure_high', 'pressure_lower')
        
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "pulse": instance.pulse,
            "timestamp": instance.timestamp,
            "pressure": {
                "lower": instance.pressure_lower,
                "high": instance.pressure_high
            }
        }
    
    def to_internal_value(self, data):
        pressure_data = data.get('pressure', {})
        pressure_serializer = PressureFieldSerializer(data=pressure_data, required=True)
        
        if pressure_serializer.is_valid():
            data["pressure_high"] = pressure_serializer.validated_data.get("high")
            data["pressure_lower"] = pressure_serializer.validated_data.get("lower")
            del data["pressure"]
        return super().to_internal_value(data)