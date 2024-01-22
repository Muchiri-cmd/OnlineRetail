from django.shortcuts import render
from django.http import HttpResponse
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,WishList,ProductImages,ProductReview,Address

# Create your views here.
def index(request):
    #products=Product.objects.all().order_by("-date")
    products=Product.objects.filter(featured=True,product_status="published")
    context={
        "products":products
    }
    return render(request,'core/index.html',context)

def product_list_view(request):
    products=Product.objects.filter(product_status="published")
    context={
        "products":products
    }
    return render(request,'core/product-list.html',context)

