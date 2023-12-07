from rest_framework import serializers
from records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'condition', 'humidity', 'temperature', 'wind', 'date')
        model = Record