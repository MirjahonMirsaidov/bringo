from django.urls import path

from utils.bringo_db import WriteToExcelView
from .views import ProductUpdateView, RestaurantsView, RestaurantView, SyncRestaurantsView, SyncRestaurantView, SyncRestaurantBySlugView, \
    SyncRestaurantProductsBySlugView, SyncProductsView, ProductsListView, ToggleActivityProductView, \
    JowiManufacturerDelete, JowiProductDelete, JowiProductConnect, JowiManufacturerConnectView, SyncronizeProductView, \
    JowiProductNotificationToggle

app_name = "bringo_db"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('restaurants/', RestaurantsView.as_view()),  # restoran list
    path('restaurant/<slug:slug>/', RestaurantView.as_view()),  # restoran detail
    path('sync/restaurants/', SyncRestaurantsView.as_view()),
    path('sync/restaurants/<slug:slug>/', SyncRestaurantBySlugView.as_view()),
    path('sync/restaurant/<slug:slug>/', SyncRestaurantView.as_view()),
    path('sync/restaurant/product/<slug:slug>/', SyncRestaurantProductsBySlugView.as_view()),
    path('restaurant/<slug:slug>/add-product/', SyncProductsView.as_view()),
    path('restaurant/<slug:slug>/products/', ProductsListView.as_view()),
    path('product/toggle_activity/', ToggleActivityProductView.as_view()),
    path('restaurant/<slug:slug>/disconnect/', JowiManufacturerDelete.as_view()),
    path('manufacturer/connects/', JowiManufacturerConnectView.as_view()),
    path('product/<slug:slug>/disconnect/', JowiProductDelete.as_view()),
    path('product/<slug:slug>/toggle-notification/', JowiProductNotificationToggle.as_view()),
    path('product/connect/', JowiProductConnect.as_view()),
    path('product/synchronize/', SyncronizeProductView.as_view()),
    path('write-excel/<slug:slug>/', WriteToExcelView.as_view()),
    path('product/update/', ProductUpdateView.as_view()),
    # path('restaurant-bringo/<slug:slug>/toggle_activity/', BringoToggleActivityRestaurantView.as_view()),
    # path('product/get/<int:id>', GetProductView.as_view()),
    # path('restaurant-single/get/<int:id>', GetRestaurantById.as_view()),
    # path('restaurant-jowi/<slug:slug>/toggle_activity/', JowiToggleActivityRestaurantView.as_view()),
]