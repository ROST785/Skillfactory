from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import PerevalAdded, Users, Coord, Images, Level


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'fam', 'name', 'otc']

    def save(self, **kwargs):
        self.is_valid()
        user = Users.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = Users.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
        return new_user


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

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user_id
            data_user = data.get('user_id')
            user_fields_for_validation = [
                instance_user.email != data_user['email'],
                instance_user.phone != data_user['phone'],
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Данные пользователя заменить нельзя',
                    }
                )
        return data

    class Meta:
        model = PerevalAdded
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'level_id', 'user_id',
                  'coord_id', 'images', 'status']
