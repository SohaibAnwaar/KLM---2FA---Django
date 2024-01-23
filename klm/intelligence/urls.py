from django.urls import path
from klm.intelligence.views import get_region_type_list, province_data_lineage, \
    get_country_province, get_province_municipality, get_municipality_district, get_district_neighbourhood

urlpatterns = [
    path('data_lineage/<str:region_code>/<str:region_name>/', province_data_lineage, name='province_data_lineage'),
    path('region_type_list/<str:region_type>/', get_region_type_list, name='get_region_type_list'),
    path('country_province/<str:country_name>/', get_country_province, name='get_country_province'),
    path('province_municipality/<str:province_name>/', get_province_municipality, name='get_province_municipality'),
    path('municipality_district/<str:municipality_name>/', get_municipality_district, name='get_municipality_district'),
    path('district_neighbourhood/<str:district_name>/', get_district_neighbourhood, name='get_district_neighbourhood'),
]
