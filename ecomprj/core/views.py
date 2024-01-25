from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,WishList,ProductImages,ProductReview,Address
from taggit.models import Tag
from taggit.managers import TaggableManager
from django.db.models import Avg
from core.forms import ProductReviewForm

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
    category_products=Product.objects.filter(category=product.category).exclude(product_id=product_id)#[:4]
    reviews=ProductReview.objects.filter(product=product).order_by("-date")
    average_rating=ProductReview.objects.filter(product=product).aggregate(average=Avg('rating'))
    make_review=True
    if request.user.is_authenticated:
        user_review_count=ProductReview.objects.filter(user=request.user,product=product).count()
        if user_review_count>0:
            make_review=False
        

    product_images=product.product_images.all()
    review_form=ProductReviewForm()
    context={
        "product":product,
        "product_images":product_images,
        "category_products":category_products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form,
        "make_review":make_review,

    }
    
    return render(request,'core/product-detail.html',context)

def tag_list(request,tag_slug=None):

    products=Product.objects.filter(product_status="published").order_by("-id")
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        products=products.filter(tags__in=[tag])

    context={
        "products":products,
        "tag":tag,
    }
    return render(request,"core/tag.html",context)

def add_review(request,product_id):
    product=Product.objects.get(product_id=product_id)
    user=request.user

    review=ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )
    context={
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
    average_reviews=ProductReview.objects.filter(product=product).aggregate(average=Avg("rating"))
    
    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'average_reviews':average_reviews
        }
       
    )