from rest_framework import serializers
from .models import HashTag


class TrendingTweetsSerialzers(serializers.ModelSerializer):
    
    trendstweetcount = serializers.SerializerMethodField()

    class Meta:
        model = HashTag
        fields = ["name","trendstweetcount"]

    def get_trendstweetcount(self, obj):
        return obj.tweet.count()
        
    