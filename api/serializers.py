from rest_framework import serializers

class WaterRecommendationSerializer(serializers.Serializer):
    state = serializers.CharField()
    crop = serializers.CharField()
    soil_type = serializers.CharField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    rainfall = serializers.FloatField()
    soil_moisture = serializers.FloatField()
    
