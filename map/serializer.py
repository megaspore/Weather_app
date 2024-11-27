
from .models import ForecastPoint, ForecastPoly
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class ForecastPointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ForecastPoint
        
        fields = '__all__'
        geo_field = "geometry"
class ForecastPolySerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = ForecastPoly
        
        fields =  '__all__'
        geo_field = "geometry"
#class Task_extendedSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = Task_extended
   #     fields = ['field_3', 'field_4', 'field_5']

#class TaskSerializer(serializers.ModelSerializer):
 #   task_extendeds = Task_extendedSerializer(many=True)
    
  #  class Meta:
   #     model = Task
    #    fields = '__all__'