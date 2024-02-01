from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,WishList,ProductImages,ProductReview,Address
from taggit.models import Tag
from taggit.managers import TaggableManager
from django.db.models import Avg
from core.forms import ProductReviewForm
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required

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

def search_view(request):
    query=request.GET['q']
    #products=Product.objects.filter(title__icontains=query,description__icontains=query).order_by("-date")#startswith 
    try:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by("-date")
    except Exception as e:
        print(f"Error: {e}")
        products = []
    context={
        "products":products,
        "query":query,

    }
    return render(request,"core/search.html",context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    products=Product.objects.filter(product_status="published").order_by("-product_id").distinct()#more specific
    min_price=request.GET['min_price']
    max_price=request.GET['max_price']

    products=products.filter(price__gte=min_price)#>=
    products=products.filter(price__lte=max_price)

   
    if len(categories)>0:
        products=products.filter(category__category_id__in=categories)

    if len(vendors)>0:
        products=products.filter(vendor__vendor_id__in=vendors).order_by("-vendor_id").distinct()

    context={
        "products":products,
        
    }

    data = render_to_string("core/async/product-list.html",context)
    return JsonResponse({
        "data":data,

    })

def add_to_cart(request):
    cart_product={}
    cart_product[str(request.GET['id'])]={#from ajax submission
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['img'],
        'pid':request.GET['pid']
    }
    if 'cart_data_obj' in request.session:#Get current active session in browser
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data
        else:
            cart_data=request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj']=cart_data
    else:
        request.session['cart_data_obj']=cart_product
    
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request,"Your cart is empty")
        return redirect("core:index")

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_quantity=request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']=product_quantity
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount=0
    #check if cart_data_obj session still exists
    if 'cart_data_obj' in request.session:
        #getting total amount for paypal
        for product_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        #Create order object
        order=CartOrder.objects.create(
             user=request.user,
             price=total_amount,
             
        )
        
        
        #Getting total for cart
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount +=int(item['qty']) * float(item['price'])
            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id), # INVOICE_NO-5,
                item=item['title'],
                image=item['image'],
                quantity=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )

            
    host=request.get_host()
    paypal_dictionary={
        "business":settings.PAYPAL_RECEIVER_EMAIL,
        "amount":cart_total_amount,
        "item_name":'Order-Item-No-'+str(order.id),
        "invoice":"INVOICE_NO-"+str(order.id),
        "currency_code":"USD",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:paymentcompleted")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:paymentfailed")),

    }
    paypal_payment_button=PayPalPaymentsForm(initial=paypal_dictionary)
    try:
        active_address=Address.objects.get(user=request.user,status=True)
    except:
          messages.warning(request, "There are multiple addresses, only one should be activated.")
            
          active_address=None

    
    return render(request,'core/checkout.html',{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount,'paypal_payment_button':paypal_payment_button,"active_address":active_address})

@login_required   
def payment_completed_view(request):
    context={}
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        context={}
    return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),
                                                          'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    context={}
    return render(request,'core/payment-failed.html',context)

@login_required
def customer_dashboard(request):
    orders=CartOrder.objects.filter(user=request.user).order_by("-id")
    address=Address.objects.filter(user=request.user)
    if request.method=="POST":
        address=request.POST.get("address")
        mobile_no=request.POST.get("mobile_no")

        new_address=Address.objects.create(
            address=address,
            mobile_no=mobile_no,
            user=request.user
        )
        messages.success(request,"Address added succesfully")
        return redirect("core:dashboard")
    context={
        "orders":orders,
        "address":address,

    }
    return render(request,'core/dashboard.html',context)

def order_detail(request,id):
    order=CartOrder.objects.get(user=request.user,id=id)
    order_items=CartOrderItems.objects.filter(order=order)

    context={
        "order_items":order_items,
        
    }
    return render(request,'core/order-details.html',context)

def make_address_defualt(request):
     id=request.GET['id']
     #Deactivate all addresses as we are selecting a new one 
     Address.objects.update(status=False)
     #Tick the selected address
     Address.objects.filter(id=id).update(status=True)
     return JsonResponse({"boolean":True})