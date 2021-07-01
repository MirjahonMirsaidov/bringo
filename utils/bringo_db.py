from io import StringIO

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from bringo_db.models import Product, StoreProductProduct, ProductImage, ProductCategory, ProductTranslate, \
    JowiProduct, Products, ManufacturerCategory, MainProductTranslate, JowiManufacturer


import io
from django.http import HttpResponse
from django.views.generic import View
import xlsxwriter


def get_product_info(li, name, prod, price=0, image=0, jowi_product=0):
    if jowi_product:
        jowi_product = {
            'name': jowi_product.title,
            'price': jowi_product.price,
            'product_id': jowi_product.product_id,
            'jowi_category_id': jowi_product.jowi_category_id,
            'jowi_id': jowi_product.jowi_id,
            'notification': jowi_product.notification
        }
    if image:
        image = image.name
    product = Product.objects.get(id=prod.object_id)
    li.append({
        'id': product.id,
        'name': prod.name,
        'is_active': product.is_active,
        'price': price,
        'image': image,
        'jowi_product': jowi_product,
        'restaurant': name
    })


def save_products(slug, manufacturer_id, course, category, jowi_category):

    product = Product.objects.create(
        manufacturer_id=manufacturer_id,
        price=course['price'],
        cook_time=course['cooking_time'],
        use_configurations=0,
        url=0,
        max_price=0,
        is_show=0,
        quantity_order=0,
        votes=0,
        rating=0,
        product_to=0,
        product_weather_type=0,
        preparation_type=0,
        posuda=0,
        paket=0
    )

    main_product = Products.objects.create(
        manufacturer_id=manufacturer_id,
    )
    
    main_product_translate = MainProductTranslate.objects.create(
        object_id=main_product.id,
        name=course['title'],
        meta_title=0,
        meta_keywords=0,
        meta_description=0
    )

    store_product_product = StoreProductProduct.objects.create(
        store_product_id=product.id,
        product_id=main_product.id
    )

    product_image = ProductImage.objects.create(
        product_id=product.id,
        url=course.get('image_url'),
        title=course['title']
    )

    product_category = ProductCategory.objects.create(
        product=product.id,
        category=category
    )

    product_translate = ProductTranslate.objects.create(
        object_id=product.id,
        name=course['title']
    )

    jowi_product = JowiProduct.objects.create(
        title=course['title'],
        price=course['price'],
        product_id=product.id,
        jowi_category_id=jowi_category.id,
        jowi_id=course['id'],
    )


def update_products(course, manufacturer_id, category):
    if JowiProduct.objects.filter(jowi_id=course['id']).exists():
        try:
            id = JowiProduct.objects.filter(jowi_id=course['id']).first().product_id
            product = Product.objects.get(id=id)
            product.price = course['price']
            product.cook_time = course['cooking_time']
            product.save()
        except ObjectDoesNotExist:

            product = Product.objects.create(
                manufacturer_id=manufacturer_id,
                price=course['price'],
                cook_time=course['cooking_time'],
                use_configurations=0,
                url=0,
                max_price=0,
                is_show=0,
                quantity_order=0,
                votes=0,
                rating=0,
                product_to=0,
                product_weather_type=0,
                preparation_type=0,
                posuda=0,
                paket=0
            )
            main_product = Products.objects.create(
                manufacturer_id=manufacturer_id,
            )

            main_product_translate = MainProductTranslate.objects.create(
                object_id=main_product.id,
                name=course['title'],
                meta_title=0,
                meta_keywords=0,
                meta_description=0
            )

            store_product_product = StoreProductProduct.objects.create(
                store_product_id=product.id,
                product_id=main_product.id
            )

            product_translate = ProductTranslate.objects.create(
                object_id=product.id,
                name=course['title']
            )
            product_category = ProductCategory.objects.create(
                product=product.id,
                category=category
            )
        try:
            product_image = ProductImage.objects.get(product_id=product.id)
            product_image.url = course.get('image_url')
            product_image.save()
        except ObjectDoesNotExist:
            product_image = ProductImage.objects.create(
                product_id=product.id,
                url=course.get('image_url'),
                title=course['title']
            )



def get_restaurant_name_by_slug(slug):
    url = "https://api.jowi.club/v010/restaurants"

    payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    restaurant = None
    for res in response['restaurants']:
        if res['id'] == slug:
            jowi_manufacturer = JowiManufacturer.objects.filter(jowi_id=res['id']).first()
            restaurant = res['title']

    return restaurant


class WriteToExcelView(APIView):

    def get(self, request, slug):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Get some data to write to the spreadsheet.
        urlm = "https://api.jowi.club/v010/restaurants"

        payloadm = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headersm = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        responsem = requests.request("GET", urlm, headers=headersm, data=payloadm)
        responsem = responsem.json()
        open_time, close_time = None, None

        for res in responsem['restaurants']:
            if res['id'] == slug:
                open_time = res['work_timetable'][0]['open_time']
                close_time = res['work_timetable'][0]['close_time']

        # Write some test data.
        url = "https://api.jowi.club/v010/restaurants/" + slug

        payload = 'api_key=%20yxb3eAEis2MYsust2eHUH_i_9DhzMb1IplTXt_kO&sig=%2018f945ea1fc9bba'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        worksheet.write('A1', "время приготовления")
        worksheet.write('B1', "наименования")
        worksheet.write('C1', "цена")
        worksheet.write('D1', "ингридиент")
        worksheet.write('D1', "время работи начало")
        worksheet.write('F1', "время работи конец")
        worksheet.write('G1', "под категория")

        i = 2
        for res in response['categories']:
            for cors in res['courses']:
                is_active = None
                if JowiProduct.objects.filter(jowi_id=cors['id']).exists():
                    jowi_product = JowiProduct.objects.filter(jowi_id=cors['id']).first()
                    if Product.objects.filter(id=jowi_product.product_id).exists():
                        if Product.objects.filter(id=jowi_product.product_id).first().is_active:
                            worksheet.write(f'A{i}', cors["cooking_time"])
                            worksheet.write(f'B{i}', cors["title"])
                            worksheet.write(f'C{i}', cors["price"])
                            worksheet.write(f'D{i}', '')
                            worksheet.write(f'E{i}', open_time)
                            worksheet.write(f'F{i}', close_time)
                            worksheet.write(f'G{i}', res['title'])

                            i += 1

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response