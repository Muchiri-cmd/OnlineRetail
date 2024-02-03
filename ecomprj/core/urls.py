from django.urls import path
from core.views import *
from django.urls import include

app_name="core"

urlpatterns=[
    path("",index,name="index"),
    path("products/",product_list_view,name="productslist"),
    path('categories/',category_list_view,name="categorieslist"),
    path("category/<category_id>/",product_list_category_view,name="categoryproductslist"),
    path("vendors/",vendor_list_view,name="vendorslist"),
    path("vendor/<vendor_id>/",vendor_detail_view,name="vendordetailsview"),
    path("product/<product_id>/",product_detail_view,name="productdetailview"),
    path("products/tags/<tag_slug>/", tag_list, name="tags"),
    path("add_review/<product_id>/",add_review,name="addreview"),
    path("search/",search_view,name="search"),
    path("filter-products/",filter_product,name="filterproducts"),
    path("add-to-cart/",add_to_cart,name="add-to-cart"),
    path("cart/",cart_view,name="cart"),
    path("delete-from-cart/",delete_item_from_cart,name="deletefromcart"),
    path("update-cart/",update_cart,name="updatecart"),
    path("checkout/",checkout_view,name="checkout"),
    path("paypal/",include('paypal.standard.ipn.urls')),
    path("payment-completed/",payment_completed_view,name="paymentcompleted"),
    path("payment-failed/",payment_failed_view,name="paymentfailed"),
    path("dashboard/",customer_dashboard,name="dashboard"),
    path("dashboard/order/<int:id>",order_detail,name="orderdetail"),
    path("make-default-address/",make_address_defualt,name="makeaddressdefualt"),
    path("wishlist/",wishlist_view,name="wishlist"),
    path("add-to-wishlist/",add_to_wishlist,name="addtowishlist"),
    

    

]