from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from bringo_db.models import JowiManufacturer, JowiProduct, ManufacturerTranslate, Product

import requests

from utils.bringo_db import get_restaurant_name_by_slug


class RestaurantsView(APIView):
    def get(self, request):
        url = "https://api.jowi.club/v010/restaurants"

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        return Response(response)


class RestaurantsWithSyncedView(APIView):
    def get(self, request):

        url = "https://api.jowi.club/v010/restaurants"

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        restaurants = []
        for restaurant in response['restaurants']:
            jowi_manufacturer = JowiManufacturer.objects.filter(jowi_id=restaurant['id']).first()
            manufacturer_id = 0
            modified = 0
            if jowi_manufacturer is not None:
                manufacturer_id = jowi_manufacturer.manufacturer_id
                modified = JowiProduct.objects.filter(product_id__in=Product.objects.filter(manufacturer_id=manufacturer_id)).aggregate(
                    modified=Sum('modified')).get('modified')
                if not modified:
                    modified = 0

            restaurants.append({
                'id': manufacturer_id,
                'jowi_id': restaurant['id'],
                'name': restaurant['title'],
                'active': False,
                'modified': modified
            })

        return Response({'success': True, 'restaurants': restaurants})


class RestaurantView(APIView):
    def get(self, request, slug):
        url = "https://api.jowi.club/v010/restaurants/" + slug

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        data = []
        manufacturer_id = JowiManufacturer.objects.filter(jowi_id=slug).first().manufacturer_id
        for res in response['categories']:
            courses = []
            for cors in res['courses']:
                try:
                    jowi_product = JowiProduct.objects.filter(jowi_id=cors['id'], product_id__in=Product.objects.filter(manufacturer_id=manufacturer_id)).first()
                    is_active = Product.objects.filter(id=jowi_product.product_id, manufacturer_id=manufacturer_id).first().is_active
                    modified = jowi_product.modified
                except:
                    modified = 0
                    is_active = None
                

                courses.append({
                    "id": cors['id'],
                    "title": cors['title'],
                    "price": cors['price'],
                    "price_for_online_order": cors['price_for_online_order'],
                    "is_exception": cors['is_exception'],
                    "online_order": cors['online_order'],
                    "is_vegetarian": cors['is_vegetarian'],
                    "cooking_time": cors['cooking_time'],
                    "caloric_content": cors['caloric_content'],
                    "description": cors['description'],
                    "count_left": cors['count_left'],
                    "image": cors.get('image_url'),
                    'is_active': is_active,
                    'modified': modified,
                })
            data.append({
                'title': res['title'],
                'courses': courses
            })
        return Response({'categories': data, 'restaurant': slug})


class RestaurantSingleView(APIView):
    def get(self, request, slug):

        url = "https://api.jowi.club/v010/restaurants"

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        restaurant = {
            'id': 0,
            'jowi_id': '',
            'name': '',
            'status': False,
        }

        for res in response['restaurants']:
            if res['id'] == slug:
                jowi_manufacturer = JowiManufacturer.objects.filter(jowi_id=res['id']).first()
                restaurant['jowi_id'] = slug
                restaurant['name'] = res['title']
                if (jowi_manufacturer != None):
                    restaurant['id'] = jowi_manufacturer.manufacturer_id
                    restaurant['bringo_restaurant'] = {
                        'id': jowi_manufacturer.manufacturer_id,
                        'jowi_id': slug,
                        'name': jowi_manufacturer.title,
                        'status': False,
                    }
                return Response({
                    'success': True,
                    'restaurant': restaurant
                })
        return Response({
            'success': False
        })


class ProductSingleView(APIView):
    def get(self, request, restaurant, product):
        url = "https://api.jowi.club/v010/restaurants/" + restaurant

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        # print(response)

        prod = {
            'manufacturer': get_restaurant_name_by_slug(restaurant),
            'title': '',
            'price': None,
            'status': False,
            'connected': False,
        }
        if JowiProduct.objects.filter(jowi_id=product).exists():
            prod['status'] = bool(JowiProduct.objects.filter(jowi_id=product).first().status)
            prod['connected'] = True

        for category in response['categories']:
            for pro in category['courses']:
                if pro['id'] == product:
                    prod['title'] = pro['title']
                    prod['price'] = pro['price']

        return Response(prod)


class JowiProductStatusChange(APIView):

    def get(self, request, slug):
        jowi_product = JowiProduct.objects.filter(jowi_id=slug).first()
        jowi_product.status = False if jowi_product.status else True
        return Response(jowi_product.status)
