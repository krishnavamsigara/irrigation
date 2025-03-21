from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(__file__), 'water_recommendation_10000.csv')
df = pd.read_csv(csv_path)

class GetRecommendations(APIView):
    def post(self, request):
        state = request.data.get('state')
        crop = request.data.get('crop')
        soil = request.data.get('soil')
        temperature = request.data.get('temperature')
        humidity = request.data.get('humidity')
        rainfall = request.data.get('rainfall')
        moisture = request.data.get('moisture')

        if not all([state, crop, soil, temperature, humidity, rainfall, moisture]):
            return Response({"error": "Please provide all fields: state, crop, soil, temperature, humidity, rainfall, moisture."}, status=status.HTTP_400_BAD_REQUEST)

        filtered = df[
            (df['State'].str.lower() == state.lower()) &
            (df['Crop'].str.lower() == crop.lower()) &
            (df['Soil_Type'].str.lower() == soil.lower())
        ]

        if filtered.empty:
            return Response({"message": "No data found for given criteria."}, status=status.HTTP_404_NOT_FOUND)

        base_water = filtered["Water_Required"].mean()

        # Example custom adjustments based on input data
        temp_factor = (float(temperature) - filtered["Temperature"].mean()) * 0.05
        humidity_factor = (filtered["Humidity"].mean() - float(humidity)) * 0.03
        rainfall_factor = (filtered["Rainfall"].mean() - float(rainfall)) * 0.02
        moisture_factor = (filtered["Soil_Moisture"].mean() - float(moisture)) * 0.04

        adjusted_water = base_water + temp_factor + humidity_factor + rainfall_factor + moisture_factor

        return Response({
            "State": state,
            "Crop": crop,
            "Soil_Type": soil,
            "Given_Temperature": temperature,
            "Given_Humidity": humidity,
            "Given_Rainfall": rainfall,
            "Given_Soil_Moisture": moisture,
            "Recommended_Water_L_per_m2_per_week": round(adjusted_water, 2)
        })
