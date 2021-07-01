import time

from django.db import connection
from django.views import generic
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

import requests
from datetime import datetime

from .models import Manufacturer, JowiManufacturer, JowiCategory, JowiProduct, JowiManufacturer, ManufacturerTranslate, \
    Category, CategoryTranslate, JowiCategory, Product, ProductTranslate, ProductImage, Products, \
    ProductCategory, ManufacturerCategory, StoreProductProduct, MainProductTranslate

from .serializers import ManufacturerSerializer, JowiManufacturerSerializer, ManufacturerTranslateSerializer, \
    CategorySerializer, CategoryTranslateSerializer, JowiCategorySerializer, ProductSerializer, \
    ProductTranslateSerializer, JowiProductSerializer, ProductImageSerializer

from utils.bringo_db import get_product_info, save_products, update_products


# need with translation and jowi model
class RestaurantsView(APIView):
    def get(self, request):
        manufacturer = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturer, many=True)
        restaurants = []
        for item in serializer.data:
            try:
                jowi_restaurant = JowiManufacturer.objects.filter(manufacturer_id=item['id']).first().jowi_id
            except:
                jowi_restaurant = None
            restaurant_translate = ManufacturerTranslate.objects.filter(object_id=item['id']).first()
            restaurant = Manufacturer.objects.get(id=item['id'])
            if restaurant_translate:
                restaurants.append({
                    'id': item['id'],
                    'jowi_id': jowi_restaurant,
                    'name': restaurant_translate.name,
                    'active': bool(restaurant.status),
                })
        return Response({'success': True, "restaurants": restaurants})


# ok
class RestaurantView(APIView):
    def get(self, request, slug):
        jowi_manufacturer_obj = None
        manufacturer_obj = None
        manufacturer_translate_obj = None
        try:
            jowi_manufacturer_obj = JowiManufacturer.objects.filter(jowi_id=slug).first()
            manufacturer_obj = Manufacturer.objects.filter(id=jowi_manufacturer_obj.manufacturer_id).first()
            manufacturer_translate_obj = ManufacturerTranslate.objects.filter(
                object_id=jowi_manufacturer_obj.manufacturer_id).first()
        except:
            pass
            # print("Model not found")
        jowi_manufacturer = JowiManufacturerSerializer(jowi_manufacturer_obj)
        manufacturer = ManufacturerSerializer(manufacturer_obj)
        manufacturer_translate = ManufacturerTranslateSerializer(manufacturer_translate_obj)
        return Response({
            'manufacturer': manufacturer.data,
            'manufacturer_translate': manufacturer_translate.data,
            'jowi_manufacturer': jowi_manufacturer.data
        })


# ok
class SyncRestaurantsView(APIView):
    def get(self, request):
        url = "https://api.jowi.club/v010/restaurants"

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        jowi_restaurants = response['restaurants']

        restaurant_saved = None
        restaurant_translate_saved = None
        jowi_restaurant_saved = None
        for restaurant in jowi_restaurants:

            try:
                jowi_restaurant_saved = JowiManufacturer.objects.get(jowi_id=restaurant['id'])
            except:
                pass
                # print("Model not found")

            if jowi_restaurant_saved is not None:
                if Manufacturer.objects.filter(id=jowi_restaurant_saved.manufacturer_id).exists():
                    restaurant_saved = Manufacturer.objects.get(id=jowi_restaurant_saved.manufacturer_id)
                    restaurant_translate_saved = ManufacturerTranslate.objects.get(
                        object_id=jowi_restaurant_saved.manufacturer_id)
            else:

                restaurant_data = {
                    'is_new': 0,
                    # layout: models.CharField(max_length=255, blank=True, null=True)
                    # view: models.CharField(max_length=255, blank=True, null=True)
                    'min_sum': 0,
                    'min_sum_order': 0,
                    'from_free_sum': 0,
                    'sum_own_delivery': restaurant['delivery_price'],
                    'opportunity_own_delivery': '',
                    'time_delivery': restaurant['delivery_time'],
                    'rating': 0,
                    'votes': 0,
                    'phone': restaurant['phone_numbers'],
                    'phone_restaurant': '',
                    'phone_manager': '',
                    'courier': '',
                    'work_start': '00:00',
                    'work_finish': '00:00',
                    'status': 1,
                    'is_recommended': 0,
                    'is_promotion': 0,
                    'site': restaurant['website'] or '',
                    'email': '',
                    'contact_name': '',
                    'created': '2000-01-01 00:00',
                    'rating_total': 0,
                    'is_type': 0,
                    'lat': restaurant['latitude'],
                    'lon': restaurant['longitude'],
                    'comment': 0,
                    'delivery_status': 0,
                    'min_distance': 0,
                    'min_distance_limit': 0.0,
                    'distance_limit_price': 0.0,
                    'price_per_min_distance': 0.0,
                    'price_per_km': 0.0,
                    'prices_per_km': '',
                    'notify_param': '',
                    'free_from': 0.0,
                    'c_min_distance': 0.0,
                    'c_price_per_min_distance': 0.0,
                    'c_prices_per_km': '',
                    'pik_prices_per_km': '',
                    'pik_time_noon': '',
                    'pik_time_launch': '',
                    'c_price_per_km': 0.0,
                    'discount_status': 0,
                    'discount_date_from': '2000-01-01 00:00',
                    'discount_date_to': '2000-01-01 00:00',
                    'pik_c_prices_per_km': '',
                    'pik_c_time_noon': '',
                    'pik_c_time_launch': '',
                    'group_id': 0,
                    'show_bot': 0,
                    'pik_min_distance': 0.0,
                    'pik_price_per_min_distance': 0.0,
                    'pik_c_min_distance': 0.0,
                    'pik_c_price_per_min_distance': 0.0,
                    'tracking': 0,
                    'middile_id': '',
                    'free_delivery_discount_bringo': 0,
                    'avto_zagatovka': 0,
                    'sum_for_discount': 0.0,
                    'discount_for_totalsum': 0.0,
                    'delivery_discount_bringo': 0.0,
                    'is_pharmacy': 0,
                    'user_id': 1
                }

                serializer = ManufacturerSerializer(data=restaurant_data)
                if serializer.is_valid(raise_exception=True):
                    restaurant_saved = serializer.save()

                restaurant_translate_data = {
                    'object_id': restaurant_saved.id,
                    'language_id': 1,
                    'name': restaurant['title'],
                    'description': restaurant['description'],
                    'full_description': restaurant['description'],
                    'meta_title': restaurant['title'],
                    'meta_keywords': '',
                    'meta_description': restaurant['description'],
                    'payment': 'Терминал, наличные',
                    'search': ''
                }
                serializer = ManufacturerTranslateSerializer(data=restaurant_translate_data)
                if serializer.is_valid(raise_exception=True):
                    restaurant_translate_saved = serializer.save()
                jowi_manufacturer_data = {
                    'title': restaurant['title'],
                    'jowi_id': restaurant['id'],
                    'manufacturer_id': restaurant_saved.id,
                    'status': 0
                }
                serializer = JowiManufacturerSerializer(data=jowi_manufacturer_data)
                if serializer.is_valid(raise_exception=True):
                    jowi_restaurant_saved = serializer.save()
            # restaurant_saved & jowi_restaurant_saved
            restaurant = ManufacturerSerializer(restaurant_saved)
            restaurant_translate = ManufacturerTranslateSerializer(restaurant_translate_saved)
            jowi_restaurant = JowiManufacturerSerializer(jowi_restaurant_saved)
            return Response({'restaurant': restaurant.data, 'restaurant_saved': restaurant_translate.data,
                             'jowi_restaurant': jowi_restaurant.data})


class SyncRestaurantView(APIView):
    def get(self, request, slug):

        url = "https://api.jowi.club/v010/restaurants/" + slug

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        categories = []
        response = response.json()

        jowi_restaurant_saved = JowiManufacturer.objects.get(jowi_id=restaurant['id'])
        restaurant_saved = Manufacturer.objects.get(id=jowi_restaurant_saved.manufacturer_id)
        restaurant_translate_saved = ManufacturerTranslate.objects.get(object_id=jowi_restaurant_saved.manufacturer_id)

        # return response
        for category in response['categories']:
            category_title = category['title']
            jowi_category_saved = None
            try:
                jowi_category_saved = JowiCategory.objects.filter(name=category_title).first()
            except:
                pass
                # print("Model not found")
            if jowi_category_saved is None:
                category_data = {
                    'lft': None,
                    'rgt': None,
                    'lavel': None,
                    'url': '',
                    'full_path': '',
                    'layout': '',
                    'view': '',
                    'decscription': category_title,
                    'position': 0,
                    'sort': '',
                    'parent': 0,
                    'sort_popularity': 0
                }

                category_object = None
                serializer = CategorySerializer(data=category_data)
                if serializer.is_valid(raise_exception=True):
                    category_object = serializer.save()

                category_translate_data = {
                    'object_id': category_object.id,
                    'language_id': 1,
                    'name': category_title,
                    'meta_title': category_title,
                    'meta_keywords': category_title,
                    'meta_description': category_title,
                    'description': category_title
                }

                category_translate_object = None
                serializer = CategoryTranslateSerializer(data=category_translate_data)
                if serializer.is_valid(raise_exception=True):
                    category_translate_object = serializer.save()

                jowi_category_data = {
                    'name': category_translate_object.name,
                    'category_id': category_object.id,
                    'status': 0
                }

                serializer = JowiCategorySerializer(data=jowi_category_data)
                if serializer.is_valid(raise_exception=True):
                    jowi_category_object = serializer.save()
            for product in category['courses']:
                jowi_product_saved = None
                try:
                    jowi_product_saved = JowiProduct.objects.filter(jowi_id=product['id']).first()
                except:
                    pass
                    # print("Model not found")

            categories.append({'title': category_title})

        return Response({'categories': categories, 'response': response})


class SyncRestaurantBySlugView(APIView):
    def get(self, request, slug):
        url = "https://api.jowi.club/v010/restaurants"

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        jowi_restaurants = response['restaurants']

        restaurant_saved = None
        restaurant_translate_saved = None
        jowi_restaurant_saved = None
        for restaurant in jowi_restaurants:
            if restaurant['id'] == slug:
                try:
                    jowi_restaurant_saved = JowiManufacturer.objects.filter(jowi_id=restaurant['id']).first()
                except:
                    pass
                    # print("Model not found")

                if jowi_restaurant_saved is not None:
                    restaurant_saved = Manufacturer.objects.get(id=jowi_restaurant_saved.manufacturer_id)
                    restaurant_translate_saved = ManufacturerTranslate.objects.get(
                        object_id=jowi_restaurant_saved.manufacturer_id)
                else:

                    restaurant_data = {
                        'is_new': 0,
                        # layout: models.CharField(max_length=255, blank=True, null=True)
                        # view: models.CharField(max_length=255, blank=True, null=True)
                        'min_sum': 0,
                        'min_sum_order': 0,
                        'from_free_sum': 0,
                        'sum_own_delivery': restaurant['delivery_price'],
                        'opportunity_own_delivery': '',
                        'time_delivery': restaurant['delivery_time'],
                        'rating': 0,
                        'votes': 0,
                        'phone': restaurant['phone_numbers'],
                        'phone_restaurant': '',
                        'phone_manager': '',
                        'courier': '',
                        'work_start': '00:00',
                        'work_finish': '00:00',
                        'status': 0,
                        'is_recommended': 0,
                        'is_promotion': 0,
                        'site': restaurant['website'] or '',
                        'email': '',
                        'contact_name': '',
                        'created': '2000-01-01 00:00',
                        'rating_total': 0,
                        'is_type': 0,
                        'lat': restaurant['latitude'],
                        'lon': restaurant['longitude'],
                        'comment': 0,
                        'delivery_status': 0,
                        'min_distance': 0,
                        'min_distance_limit': 0.0,
                        'distance_limit_price': 0.0,
                        'price_per_min_distance': 0.0,
                        'price_per_km': 0.0,
                        'prices_per_km': '',
                        'notify_param': '',
                        'free_from': 0.0,
                        'c_min_distance': 0.0,
                        'c_price_per_min_distance': 0.0,
                        'c_prices_per_km': '',
                        'pik_prices_per_km': '',
                        'pik_time_noon': '',
                        'pik_time_launch': '',
                        'c_price_per_km': 0.0,
                        'discount_status': 0,
                        'discount_date_from': '2000-01-01 00:00',
                        'discount_date_to': '2000-01-01 00:00',
                        'pik_c_prices_per_km': '',
                        'pik_c_time_noon': '',
                        'pik_c_time_launch': '',
                        'group_id': 0,
                        'show_bot': 0,
                        'pik_min_distance': 0.0,
                        'pik_price_per_min_distance': 0.0,
                        'pik_c_min_distance': 0.0,
                        'pik_c_price_per_min_distance': 0.0,
                        'tracking': 0,
                        'middile_id': '',
                        'free_delivery_discount_bringo': 0,
                        'avto_zagatovka': 0,
                        'sum_for_discount': 0.0,
                        'discount_for_totalsum': 0.0,
                        'delivery_discount_bringo': 0.0,
                        'is_pharmacy': 0,
                        'user_id': 0
                    }

                    serializer = ManufacturerSerializer(data=restaurant_data)
                    if serializer.is_valid(raise_exception=True):
                        restaurant_saved = serializer.save()

                    restaurant_translate_data = {
                        'object_id': restaurant_saved.id,
                        'language_id': 1,
                        'name': restaurant['title'],
                        'description': restaurant['description'],
                        'full_description': restaurant['description'],
                        'meta_title': restaurant['title'],
                        'meta_keywords': '',
                        'meta_description': restaurant['description'],
                        'payment': 'Терминал, наличные',
                        'search': ''
                    }
                    serializer = ManufacturerTranslateSerializer(data=restaurant_translate_data)
                    if serializer.is_valid(raise_exception=True):
                        restaurant_translate_saved = serializer.save()
                    jowi_manufacturer_data = {
                        'title': restaurant['title'],
                        'jowi_id': restaurant['id'],
                        'manufacturer_id': restaurant_saved.id,
                        'status': 0
                    }
                    serializer = JowiManufacturerSerializer(data=jowi_manufacturer_data)
                    if serializer.is_valid(raise_exception=True):
                        jowi_restaurant_saved = serializer.save()

                restaurant = ManufacturerSerializer(restaurant_saved)
                restaurant_translate = ManufacturerTranslateSerializer(restaurant_translate_saved)
                jowi_restaurant = JowiManufacturerSerializer(jowi_restaurant_saved)
                return Response({
                    'success': True,
                    'restaurant': {
                        'restaurant': restaurant.data,
                        'restaurant_translate': restaurant_translate.data,
                        'jowi_restaurant': jowi_restaurant.data
                    }
                })
        return Response({'success': False})


class SyncRestaurantProductsBySlugView(APIView):
    def get(self, request, slug):
        url = "https://api.jowi.club/v010/restaurants/" + slug

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        jowi_restaurant = None
        try:
            jowi_restaurant = JowiManufacturer.objects.filter(jowi_id=slug).first()
        except:
            pass
            # print("Model not found")

        if jowi_restaurant is not None:
            # return response
            for category in response['categories']:
                category_title = category['title']
                category_data = {
                    'lft': None,
                    'rgt': None,
                    'lavel': None,
                    'url': '',
                    'full_path': '',
                    'layout': '',
                    'view': '',
                    'decscription': category_title,
                    'position': 0,
                    'sort': '',
                    'parent': 0,
                    'sort_popularity': 0
                }

                category_object = None
                serializer = CategorySerializer(data=category_data)
                if serializer.is_valid(raise_exception=True):
                    category_object = serializer.save()

                category_translate_data = {
                    'object_id': category_object.id,
                    'language_id': 1,
                    'name': category_title,
                    'meta_title': category_title,
                    'meta_keywords': category_title,
                    'meta_description': category_title,
                    'description': category_title
                }

                category_translate_object = None
                serializer = CategoryTranslateSerializer(data=category_translate_data)
                if serializer.is_valid(raise_exception=True):
                    category_translate_object = serializer.save()

                jowi_category_data = {
                    'name': category_translate_object.name,
                    'category_id': category_object.id,
                    'status': 0
                }

                serializer = JowiCategorySerializer(data=jowi_category_data)
                if serializer.is_valid(raise_exception=True):
                    jowi_category_object = serializer.save()
                for product in category['courses']:
                    product_data = {
                        'manufacturer_id': jowi_restaurant.manufacturer_id,
                        'type_id': 0,
                        'use_configurations': 0,
                        'url': '',
                        'price': product['price'],
                        'max_price': product['price_for_online_order'],
                        'is_weight': 0,
                        'is_active': True,
                        'is_show': False,
                        'layout': '',
                        'view': '',
                        'sku': '',
                        'quantity': product['count_left'],
                        'quantity_order': 0,
                        'availability': 0,
                        'auto_decrease_quantity': 0,
                        'work_start': '00:00',
                        'work_finish': '00:00',
                        'views_count': 0,
                        'created': '2000-01-01 00:00',
                        'updated': '2000-01-01 00:00',
                        'date_start': '00:00',
                        'date_finish': '00:00',
                        'added_to_cart_count': 0,
                        'votes': 0,
                        'rating': 0,
                        'discount': '',
                        'video': '',
                        'product_to': 0,
                        'product_weather_type': 0,
                        'dislike': 0,
                        'like': 0,
                        'comment': 0,
                        'cook_time': 0,
                        'cook_days': 0,
                        'urgent': 0,
                        'preparation_type': 0,
                        'posuda': '',
                        'paket': '',
                        'middile_id': ''
                    }
                    serializer = ProductSerializer(data=product_data)
                    product_saved = None
                    if serializer.is_valid(raise_exception=True):
                        product_saved = serializer.save()
                    if product_saved is not None:
                        product_translate_data = {
                            'object_id': product_saved.id,
                            'language_id': 1,
                            'name': product['title'],
                            'short_description': product['description'],
                            'full_description': product['description'],
                            'meta_title': product['title'],
                            'meta_keywords': product['title'],
                            'meta_description': product['description'],
                            'ingredients': '',
                        }
                        serializer = ProductTranslateSerializer(data=product_translate_data)
                        product_translate_saved = None
                        if serializer.is_valid(raise_exception=True):
                            product_translate_saved = serializer.save()
                        jowi_product_data = {
                            'title': product['title'],
                            'price': product['price'],
                            'product_id': product_saved.id,
                            'jowi_category_id': category_object.id,
                            'jowi_id': product['id'],
                            'status': 1,
                        }
                        serializer = JowiProductSerializer(data=jowi_product_data)
                        product_translate_saved = None
                        if serializer.is_valid(raise_exception=True):
                            product_translate_saved = serializer.save()

        return Response({'success': False})


class SyncProductsView(APIView):

    def get(self, request, slug):
        url = "https://api.jowi.club/v010/restaurants/" + slug

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        if JowiManufacturer.objects.filter(jowi_id=slug).exists():
            manufacturer_id = int(JowiManufacturer.objects.get(jowi_id=slug).manufacturer_id)

            for category in response['categories']:
                title = category['title']
                courses = category['courses']
                manufacturer_category = ManufacturerCategory.objects.filter(manufacturer_id=manufacturer_id)
                manufacturer_category_ids = [mc.category_id for mc in manufacturer_category]
                if not CategoryTranslate.objects.filter(name=title, object_id__in=manufacturer_category_ids).exists():
                    category = Category.objects.create(
                        position=0,
                        sort=0
                        )
                    category_translate = CategoryTranslate.objects.create(
                        object_id=category.id,
                        name=title
                    )
                    ManufacturerCategory.objects.create(manufacturer_id=manufacturer_id, category_id=category.id)

                else:

                    category = CategoryTranslate.objects.filter(name=title, object_id__in=manufacturer_category_ids).first()

                    if not ManufacturerCategory.objects.filter(manufacturer_id=manufacturer_id,
                                                               category_id=category.id).exists():
                        ManufacturerCategory.objects.fitler(manufacturer_id=manufacturer_id, category_id=category.id)
                jowi_category = JowiCategory.objects.get_or_create(
                        name=title,
                        category_id=category.id
                    )[0]

                for course in courses:

                    if JowiProduct.objects.filter(jowi_id=course['id']).exists() and Product.objects.filter(id=JowiProduct.objects.filter(jowi_id=course['id']).first().product_id, manufacturer_id=manufacturer_id).exists():
                        update_products(course, manufacturer_id, category.id)
                    else:
                        save_products(slug, manufacturer_id, course, category.id, jowi_category)

            return Response(status=status.HTTP_200_OK)
        return Response("Ushbu restoran bog'lanmagan'")


class ProductsListView(APIView):

    def get(self, request, slug):

        if JowiManufacturer.objects.filter(jowi_id=slug).exists():
            name = JowiManufacturer.objects.filter(jowi_id=slug).first().title
            id = int(JowiManufacturer.objects.get(jowi_id=slug).manufacturer_id)
            products = Product.objects.filter(manufacturer_id=id)  # .values('id', 'price')
            data = []
            for category in ManufacturerCategory.objects.filter(manufacturer_id=id):
                courses = []
                for product in products:
                    jowi_product = None
                    image = None
                    if ProductCategory.objects.filter(category=category.category_id, product=product.id).exists():
                        if ProductTranslate.objects.filter(object_id=product.id).exists():
                            prod = ProductTranslate.objects.filter(object_id=product.id).first()
                            if JowiProduct.objects.filter(product_id=product.id).exists():
                                jowi_product = JowiProduct.objects.filter(product_id=product.id).first()
                            if ProductImage.objects.filter(product_id=product.id).exists():
                                image = ProductImage.objects.filter(product_id=product.id).first()
                            get_product_info(courses, name, prod, product.price, image, jowi_product)
                data.append({
                    'title': CategoryTranslate.objects.filter(object_id=category.category_id).first().name,
                    'courses': courses
                })

            return Response(data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ToggleActivityProductView(APIView):

    def post(self, request):
        products = request.data.get('products')
        action = request.data.get('action')
        slug = request.data.get('slug')
        # try:
        manufacturer = JowiManufacturer.objects.filter(jowi_id=slug).first()
        if action == 'toggle':
            for item in products:
                if JowiProduct.objects.filter(jowi_id=item).exists():
                    jowi_product = JowiProduct.objects.filter(jowi_id=item,  product_id__in=Product.objects.filter(manufacturer_id=manufacturer.manufacturer_id)).first().product_id
                    product = Product.objects.filter(id=jowi_product, manufacturer_id=manufacturer.manufacturer_id).first()
                    product.is_active = False if product.is_active else True
                    product.save()
        elif action == 'activate':
            for item in products:
                if JowiProduct.objects.filter(jowi_id=item).exists():
                    jowi_product = JowiProduct.objects.filter(jowi_id=item,  product_id__in=Product.objects.filter(manufacturer_id=manufacturer.manufacturer_id)).first().product_id
                    product = Product.objects.filter(id=jowi_product, manufacturer_id=manufacturer.manufacturer_id).first()
                    product.is_active = True
                    product.save()
        elif action == 'deactivate':
            for item in products:
                if JowiProduct.objects.filter(jowi_id=item).exists():
                    jowi_product = JowiProduct.objects.filter(jowi_id=item,  product_id__in=Product.objects.filter(manufacturer_id=manufacturer.manufacturer_id)).first().product_id
                    product = Product.objects.filter(id=jowi_product, manufacturer_id=manufacturer.manufacturer_id).first()
                    product.is_active = False
                    product.save()
        return Response(status=status.HTTP_200_OK)
        # except:
        #     return Response('Xatolik yuz berdi', status=status.HTTP_400_BAD_REQUEST)


class JowiManufacturerDelete(APIView):

    def delete(self, request, slug):
        if JowiManufacturer.objects.filter(jowi_id=slug).exists():
            jowi_manufacturer = JowiManufacturer.objects.filter(jowi_id=slug).first()
            jowi_manufacturer.delete()
            return Response("Muvaffaqiyatli uzildi", status=status.HTTP_200_OK)
        return Response("Bog'lanish mavjud emas")


class JowiManufacturerConnectView(APIView):

    def post(self, request):
        try:
            manufacturer_id = request.data.get('id')
            title = request.data.get('name')
            jowi_id = request.data.get('jowi_id')
            if not JowiManufacturer.objects.filter(manufacturer_id=manufacturer_id, jowi_id=jowi_id).exists():
                data = {
                    'manufacturer_id': manufacturer_id,
                    'title': title,
                    'jowi_id': jowi_id,
                    'status': 1
                }
                jowi_manufacturer = JowiManufacturerSerializer(data=data)
                if jowi_manufacturer.is_valid():
                    if not JowiManufacturer.objects.filter(jowi_id=jowi_id).exists():
                        jowi_manufacturer.save()
                        return Response("Muvaffaqiyatli bog'landi", status=status.HTTP_200_OK)
                    return Response("Ushbu restoran bog'langan")
                return Response("Malumotlarni tekshirib qaytadan urinib koring", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Ushbu restoran bog'langan")
        except:
            return Response("Xatolik yuz berdi", status=status.HTTP_400_BAD_REQUEST)


class JowiProductDelete(APIView):

    def delete(self, request, slug):
        try:
            jowi_manufacturer = JowiProduct.objects.filter(jowi_id=slug)
            jowi_manufacturer.delete()
            return Response("Muvaffaqiyatli uzildi", status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JowiProductConnect(APIView):

    def post(self, request):
        try:
            product_id = request.data.get('id')
            name = request.data.get('name')
            price = request.data.get('price')
            jowi_id = request.data.get('jowi_id')
            category = ProductCategory.objects.filter(product=product_id).first().category
            jowi_category_id = JowiCategory.objects.filter(category_id=category).first().id

            if not JowiProduct.objects.filter(jowi_id=jowi_id).exists():
                jowi_product = JowiProductSerializer(
                    data={
                        'product_id': product_id,
                        'title': name,
                        'price': price,
                        'jowi_category_id': jowi_category_id,
                        'jowi_id': jowi_id,
                        'notification': 0,
                    }
                )
                if jowi_product.is_valid():
                    jowi_product.save()
                    return Response("Muvaffaqiyatli bog'landi", status=status.HTTP_201_CREATED)
                return Response(jowi_product.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Ushbu tovar bog'langan")
        except:
            return Response("Xatolik yuz berdi, iltimos malumotlarni tekshirib qaytadan urinib koring", status=status.HTTP_400_BAD_REQUEST)


class SyncronizeProductView(APIView):

    def post(self, request):
        try:
            bringo_product_id = request.data.get('bringo_product_id')
            jowi_id = request.data.get('jowi_id')
            name = request.data.get('name')
            price = request.data.get('price')
            image = request.data.get('image')
            if JowiProduct.objects.filter(product_id=bringo_product_id).exists():
                jowi_product = JowiProduct.objects.filter(product_id=bringo_product_id).first()
                jowi_product.title = name
                jowi_product.price = price
                jowi_product.jowi_id = jowi_id
                jowi_product.save()
                if ProductTranslate.objects.filter(object_id=bringo_product_id).exists():
                    product_translate = ProductTranslate.objects.filter(object_id=bringo_product_id).first()
                    product_translate.name = name
                    product_translate.save()
                    product = Product.objects.filter(id=product_translate.object_id).first()
                    product.price = price
                    product.save()
                    product_image = ProductImage.objects.filter(product_id=bringo_product_id).first()
                    product_image.url = image
                    product_image.save()

                if StoreProductProduct.objects.filter(store_product_id=bringo_product_id).exists():
                    store_product_product = StoreProductProduct.objects.filter(store_product_id=bringo_product_id).first()
                    main_product_translate = MainProductTranslate.objects.filter(object_id=store_product_product.product_id).first()
                    main_product_translate.name = name
                    main_product_translate.save()
                return Response("Muvaffaqiyatli sinxronlashtirildi")
            return Response("Bringodan tanlangan tovar jowi ga bog'lanmagan. Sinxronlash uchun avval bringodagi ushbu "
                            "tovarni bog'lang", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Xatolik yuz berdi", status=status.HTTP_400_BAD_REQUEST)


class JowiProductNotificationToggle(APIView):
    def get(self, request, slug):
        try:
            jowi_product = JowiProduct.objects.filter(jowi_id=slug).first()
            jowi_product.notification = False if jowi_product.notification else True
            jowi_product.save()
            response = "Bildirishnoma yoqildi" if jowi_product.notification else "Bildirishnoma o'chirildi"
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response("Xatolik yuz berdi", status=status.HTTP_200_OK)


class ProductUpdateView(APIView):
    def post(self, request):
        try:
            bringo_product_id = request.data.get('bringo_product_id')
            jowi_product_id = request.data.get('jowi_product_id')
            name = request.data.get('name')
            price = request.data.get('price')
            product = Product.objects.filter(id=bringo_product_id).first()
            product.price = price
            product.save()
            product_translate = ProductTranslate.objects.filter(object_id=bringo_product_id).first()
            product_translate.name = name
            product_translate.save()
            jowi_product = JowiProduct.objects.filter(jowi_id=jowi_product_id).first()
            jowi_product.price = price
            jowi_product.modified += 1
            jowi_product.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response('Xatolik yuz berdi! Malumotlarni tekshirib qaytadan kiriting', status=status.HTTP_400_BAD_REQUEST)


# class GetProductView(APIView):
#
#     def get(self, request, id):
#         product = Product.objects.filter(id=id).first()
#         product_translate = ProductTranslate.objects.filter(object_id=id).first()
#         manufacturer = ManufacturerTranslate.objects.filter(object_id=product.manufacturer_id).first()
#         jowi_id = None
#         if JowiProduct.objects.filter(product_id=id).exists():
#             jowi_id = JowiProduct.objects.filter(product_id=id).first().jowi_id
#         exists = False
#         if JowiProduct.objects.filter(product_id=id).exists():
#             exists = True
#         return Response({
#             'manufacturer': manufacturer.name,
#             'name': product_translate.name,
#             'price': product.price,
#             'is_active': product.is_active,
#             'connected': exists,
#             'jowi_id': jowi_id
#         })


# class GetRestaurantById(APIView):
#
#     def get(self, request, id):
#         res = {
#             'name': None,
#             'jowi_id': None
#         }
#         if ManufacturerTranslate.objects.filter(object_id=id).exists():
#             res['name'] = ManufacturerTranslate.objects.filter(object_id=id).first().name
#         if JowiManufacturer.objects.filter(manufacturer_id=id).exists():
#             res['jowi_id'] = JowiManufacturer.objects.filter(manufacturer_id=id).first().jowi_id
#         return Response(res)


# class BringoToggleActivityRestaurantView(APIView):
#
#     def get(self, request, slug):
#         manufacturer_id = JowiManufacturer.objects.get(jowi_id=slug).manufacturer_id
#         manufacturer = Manufacturer.objects.get(id=manufacturer_id)
#         manufacturer.status = False if manufacturer.status else True
#         manufacturer.save()
#         return Response(manufacturer.status, status=status.HTTP_200_OK)
#
# class JowiToggleActivityRestaurantView(APIView):
#
#     def get(self, request, slug):
#         manufacturer = JowiManufacturer.objects.get(jowi_id=slug)
#         manufacturer.status = False if manufacturer.status else True
#         manufacturer.save()
#         return Response(manufacturer.status, status=status.HTTP_200_OK)
#
