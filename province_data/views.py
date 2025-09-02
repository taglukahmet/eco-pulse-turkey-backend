from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from .utils import *



class CityAllView(APIView):
    def get(self,request):
        cities = City.objects.all()
        if not cities.exists():
            return Response({"detail":"Something went wrong there are no cities yet"}, status=status.HTTP_404_NOT_FOUND)
        for city in cities:
            city = prepare_city(city.id)
        serializer = CityPreSerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CityOnlyView(APIView):
    def get(self, request, city_id):
        try:
            city = City.objects.get(id = city_id)
        except City.DoesNotExist():
            return Response({"detail":"Something went wrong, city not found"}, status=status.HTTP_404_NOT_FOUND)
        city = prepare_city(city_id)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CityCompareView(APIView):
    def post(self, request):
        cities_list=[]
        for val in list(request.data.values())[0]:
            cities_list.append(val)
        cities = City.objects.filter(id__in=cities_list)
        if not cities.exists():
            return Response({"detail":"Something went wrong there are no cities yet"}, status=status.HTTP_404_NOT_FOUND)
        for city in cities:
            city = prepare_city(city.id)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FiltersView(APIView):
    def get(self, request):
        cities = City.objects.all()
        if not cities.exists():
            return Response({"detail":"Something went wrong there are no cities yet"}, status=status.HTTP_404_NOT_FOUND)
        hashtags_list = create_global_hashtags(cities)
        return Response(hashtags_list, status=status.HTTP_200_OK)
    
class NationalDataView(APIView):
    def get(self, request):
        cities = City.objects.all()
        if not cities.exists():
            return Response({"detail":"Something went wrong there are no cities yet"}, status=status.HTTP_404_NOT_FOUND)
        nationalHashtags = create_global_hashtags(cities)
        nationalHashtags = nationalHashtags[0:10]
        sentiment = generate_global_sentiment(cities)
        topTopics = create_global_topics(cities)
        topTopics = topTopics[0:10]
        nationalData = {"sentiment":sentiment, "topTopics":topTopics, "nationalHashtags":nationalHashtags}
        return Response(nationalData, status=status.HTTP_200_OK)
    
class NationalTrendsView(APIView):
    def get(self, request):
        nationalTrends = generate_national_weekly_trends()
        return Response(nationalTrends, status=status.HTTP_200_OK)
    
class RegionalPerformanceView(APIView):
    def get(self, request):
        regionalData = generate_regional_performance()
        return Response(regionalData, status=status.HTTP_200_OK)
    
class NationalSocialView(APIView):
    def get(self, request):
        nationalSocial = generate_national_social()
        weeklyComparison = generate_weekly_social()
        nationalComparison = {"nationalSocial":nationalSocial, "weeklyComparison":weeklyComparison}
        return Response(nationalComparison, status=status.HTTP_200_OK)
    
class SocialComparisonView(APIView):
    def get(self, request, city_id):
        try:
            city = City.objects.get(id = city_id)
        except City.DoesNotExist():
            return Response({"detail":"Something went wrong, city not found"}, status=status.HTTP_404_NOT_FOUND)
        socialComparison = generate_city_social(city.id)
        return Response(socialComparison, status=status.HTTP_200_OK)

        
    
    




