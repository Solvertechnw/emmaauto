from rest_framework import serializers
from cars.models import Car, CarImage

class CarImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = CarImage
        fields = ['id','image_url','alt','order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = ['id','title','slug','description','price','make','model','year','mileage','images']
