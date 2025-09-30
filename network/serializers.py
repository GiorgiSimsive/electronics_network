from rest_framework import serializers
from .models import NetworkUnit, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkUnitSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(read_only=True)
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )

    class Meta:
        model = NetworkUnit
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "products",
            "debt",
            "created_at",
            "level",
        ]
        read_only_fields = ["created_at", "level"]

    def update(self, instance, validated_data):
        """
        Требование: запретить ОБНОВЛЕНИЕ field 'debt' через API.
        (Создавать с debt можно, но при update — игнорируем.)
        """
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)
