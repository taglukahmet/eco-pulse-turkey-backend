from .models import *
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .utils import generate_city_weekly_trends

class CityPreSerializer(serializers.ModelSerializer):
    sentiment = serializers.JSONField
    hashtags = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'mainHashtag', 'sentiment', 'inclination', 'hashtags', 'region', 'd')
        read_only_fields = ('id', 'name', 'd', 'region')
        model = City

    def get_hashtags(self, obj):
        if obj.hashtags_list and isinstance(obj.hashtags_list, dict):
            return list (obj.hashtags_list.keys())
        return []
    
class CitySerializer(serializers.ModelSerializer):
    hashtags = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()
    sentiment = serializers.SerializerMethodField()
    weeklyTrend = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'sentiment', 'hashtags', 'topics', 'weeklyTrend')
        read_only_fields = ('id', 'name')
        model = City

    def get_hashtags(self, obj):
        if obj.hashtags_list and isinstance(obj.hashtags_list, dict):
            return list (obj.hashtags_list.keys())
        return []
    def get_topics(self, obj):
        if obj.topics_list and isinstance(obj.topics_list, dict):
            return list (obj.topics_list.keys())
        return []
    def get_sentiment(self, obj):
        if obj.sentiment and isinstance(obj.sentiment, dict):
            total = 0
            for val in obj.sentiment.values():
                total += val
            pozitif = (float(int((obj.sentiment["Pozitif"]/total)*10000)))/100
            notr = (float(int((obj.sentiment["Nötr"]/total)*10000)))/100
            negatif = (float(int((obj.sentiment["Negatif"]/total)*10000)))/100
            sentiment = {"positive":pozitif,"neutral":notr,"negative":negatif}
            return sentiment
    def get_weeklyTrend(self, obj):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        try:
            platforms = DataofPlatforms.objects.filter(city = obj, date=today)
        except not platforms.exists():
            try:
                platforms = DataofPlatforms.objects.filter(city = obj, date=yesterday)
            except not platforms.exists():
                return []
        weeklyTrend = generate_city_weekly_trends(obj.id)
        return weeklyTrend