from django.shortcuts import render,get_object_or_404
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

def category_list_view(request):


    categories=Category.objects.all()

    context={
        "categories":categories
    }

    return render(request,'core/categories_list.html',context)

def product_list_category_view(request,category_id):
    category_products=Category.objects.get(category_id=category_id)
    products=Product.objects.filter(product_status="published",category=category_products)
    context={
        "category_products":category_products,
        "products":products
    }
    return render(request,"core/categories-productlist.html",context)

def vendor_list_view(request):
    vendors=Vendor.objects.all()
    context={
        "vendors":vendors,
    }
    return render(request,"core/vendors_list.html",context)

def vendor_detail_view(request,vendor_id):
    vendor=Vendor.objects.get(vendor_id=vendor_id)
    products=Product.objects.filter(vendor=vendor,product_status="published")
    context={
        "vendor":vendor,
        "products":products,
    }
    return render(request,'core/vendor-details.html',context)

def product_detail_view(request,product_id):
    #product=Product.objects.get_object_or_404(Product,product_id=product_id)
    product=Product.objects.get(product_id=product_id)
    product_images=product.product_images.all()
    context={
        "product":product,
        "product_images":product_images,

    }
    
    return render(request,'core/product-detail.html',context)

    