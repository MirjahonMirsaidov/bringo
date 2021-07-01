from django.urls import path

from .views import RestaurantsView, RestaurantView, RestaurantsWithSyncedView, RestaurantSingleView, ProductSingleView,\
                JowiProductStatusChange

app_name = "jowi"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('restaurants/', RestaurantsView.as_view()),
    path('restaurants-with-synced/', RestaurantsWithSyncedView.as_view()),
    path('restaurant/get/<slug:slug>/', RestaurantSingleView.as_view()),
    path('restaurant/<slug:slug>/', RestaurantView.as_view()),
    path('product/<slug:restaurant>/<slug:product>', ProductSingleView.as_view()),
    path('product/change-status/<slug:slug>', JowiProductStatusChange.as_view()),
]