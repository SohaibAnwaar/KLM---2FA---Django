from rest_framework import serializers
from klm.intelligence.models import Region, VioScoreTotal, Dimension


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


class VioScoreTotalSerializer(serializers.ModelSerializer):
    dimensions = DimensionSerializer(many=True, read_only=True)

    class Meta:
        model = VioScoreTotal
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    vio_score_totals = VioScoreTotalSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = '__all__'
