from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import PerevalAdded, Users, Coord, Images, Level


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['mail', 'phone', 'fam', 'name', 'otc']


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PerevalAddedSerializer(WritableNestedModelSerializer):
    user_id = UsersSerializer()
    coord_id = CoordSerializer()
    level_id = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'level_id', 'user_id',
                  'coord_id', 'images', 'status']
