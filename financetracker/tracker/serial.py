from rest_framework import serializers
from .models import DebtEntry
class DebtEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtEntry
        fields = '__all__'


