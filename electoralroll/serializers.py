from django.db.models import fields
from .models import *
from rest_framework import serializers


class CitiesSer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class LegislativeAssemblySer(serializers.ModelSerializer):
    class Meta:
        model = LegislativeAssembly
        fields = "__all__"

class PartNumberSer(serializers.ModelSerializer):
    class Meta:
        model = PartNumber
        fields = "__all__"

class VoterSer(serializers.ModelSerializer):
    part = serializers.SlugRelatedField(
        slug_field="id",
        queryset=PartNumber.objects.all(),
        many=False
    )

# class HouseSer(serializers.ModelSerializer):
#     part = serializers.SlugRelatedField(
#         slug_field="id",
#         queryset=PartNumber.objects.all(),
#         many=False
#     )

    class Meta:
        model = Voter
        fields = "__all__"
