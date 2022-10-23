from rest_framework import serializers

from ads.models import Ad, Selection, Category
from ads.validators import is_published_not_true


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[is_published_not_true])
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Ad
        fields = "__all__"


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdDetailSerializer(many=True)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
