from rest_framework import serializers

from users.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()
    location = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "role", "age", "location", "total_ads"]


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        exclude = ["password"]


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location")

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        location, _ = Location.objects.get_or_create(name=self._location)
        validated_data["location"] = location

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    location = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location", "")

        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        location, _ = Location.objects.get_or_create(name=self._location)
        validated_data = {**self.validated_data, **kwargs, "location": location}
        self.instance = self.update(self.instance, validated_data)
        self.instance.set_password(validated_data["password"])
        self.instance.save()

        return self.instance


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
