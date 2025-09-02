from django.urls import path
from .views import *


urlpatterns = [
    path('provinces/', CityAllView.as_view(), name='get_all_cities_when_init_site'),
    path('provinces/<uuid:city_id>/data/', CityOnlyView.as_view(), name='get_city_when_clicked'),
    path('provinces/<uuid:city_id>/realtime/', CityOnlyView.as_view(), name='get_city_real_time'),
    path('provinces/compare/', CityCompareView.as_view(), name='post_city_compare'),
    path('filters/', FiltersView.as_view(), name='get_filters'),
    path('national-agenda/', NationalDataView.as_view(), name='get_national_main_data'),
    path('national-agenda/weekly-trends/', NationalTrendsView.as_view(), name='get_national_trends_data'),
    path('national-agenda/regional-performance/', RegionalPerformanceView.as_view(), name='get_regional_performances'),
    path('national-agenda/platform-comparison/', NationalSocialView.as_view(), name='get_national_social_comparison'),
    path('social-media/city/<uuid:city_id>/', SocialComparisonView.as_view(), name='get_city_social_comparison')

]




