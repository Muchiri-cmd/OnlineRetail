from django.urls import path
from core.views import *

app_name="core"

urlpatterns=[
    path("",index,name="index"),
    path("products/",product_list_view,name="productslist"),
    path('categories/',category_list_view,name="categorieslist"),
    path("category/<category_id>/",product_list_category_view,name="categoryproductslist")
]