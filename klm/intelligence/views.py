from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from klm.intelligence.neo4j.utils import data_lineage_province, region_type_list, query_country_province, \
    query_province_municipality, query_municipality_district, query_district_neighbourhood
from klm.intelligence.neo4j.neo4j_client import get_db_driver

db_driver = get_db_driver()
#
# from .models import Region, VioScoreTotal, Dimension
# from .serializers import RegionSerializer, VioScoreTotalSerializer, DimensionSerializer
#
#
# @extend_schema(tags=["intelligence"])
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def data_lineage_province(request, region_code, region_name):
#     try:
#         region = Region.nodes.get(code=region_code, name=region_name)
#         serializer = RegionSerializer(region)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Region.DoesNotExist:
#         return Response({"detail": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
#
#
# @extend_schema(tags=["intelligence"])
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_region_type_list(request, region_type):
#     try:
#         regions = Region.nodes.filter(type=region_type)
#         serializer = RegionSerializer(regions, many=True)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"detail": "No regions found for the specified type",
#                          "error": f"{str(e)}"}, status=status.HTTP_404_NOT_FOUND)
#


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def province_data_lineage(request, region_code, region_name):
    response = data_lineage_province(db_driver, region_name, region_code)
    if response is None:
        return Response({"detail": "Region name and or code are not found in the database"},
                        status=status.HTTP_404_NOT_FOUND)

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_region_type_list(request, region_type):
    response = region_type_list(db_driver, region_type)
    return Response(response, status=status.HTTP_200_OK)


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_country_province(request, country_name):
    response = query_country_province(db_driver, country_name)
    return Response(response, status=status.HTTP_200_OK)


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_province_municipality(request, province_name):
    response = query_province_municipality(db_driver, province_name)
    return Response(response, status=status.HTTP_200_OK)


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_municipality_district(request, municipality_name):
    response = query_municipality_district(db_driver, municipality_name)
    return Response(response, status=status.HTTP_200_OK)


@extend_schema(tags=["intelligence"])
@api_view(['GET'])
@permission_classes([AllowAny])
def get_district_neighbourhood(request, district_name):
    response = query_district_neighbourhood(db_driver, district_name)
    return Response(response, status=status.HTTP_200_OK)
