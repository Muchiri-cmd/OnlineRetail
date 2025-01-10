from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,WishList,ProductImages,ProductReview,Address
from django.db.models import Min,Max
from django.contrib import messages
def default(request):
    categories=Category.objects.all()
    vendors=Vendor.objects.all()
    min_max_price=Product.objects.aggregate(Min("price"),Max("price"))
    try:
        wishlist=WishList.objects.filter(user=request.user)
    except:
        messages.warning(request,"You are currently not logged in. Log in to access all features.")
        wishlist=0
    try:
        address=Address.objects.get(user=request.user)
    except:
        address=None
    return {
        'categories':categories,
        'address':address,
        'vendors':vendors,
        'min_max_price':min_max_price,
        'wishlist':wishlist,
    }