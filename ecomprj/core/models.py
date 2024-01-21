from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE=(
    ("process","Processing"),
    ("intransit","In-Transit"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
)
STATUS=(
    ("draft","Drafr"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("inreview","in Review"),
    ("published","Published")
)

RATING=(
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
)
def user_dir_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)
# Create your models here.
class Category(models.Model):
    category_id=ShortUUIDField(unique=True,length=10,max_length=20,prefix="CAT",alphabet="abcdefgh12345")
    title=models.CharField(max_length=100,default="Accessories")
    image=models.ImageField(upload_to="category",default="category.jpg")

    class Meta:
        verbose_name_plural="Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
     vendor_id=ShortUUIDField(unique=True,length=10,max_length=20,prefix="VEN",alphabet="abcdefgh12345")
     title=models.CharField(max_length=100,default="Mix&Pix")
     image=models.ImageField(upload_to=user_dir_path,default="vendor.jpg")
     description=models.TextField(null=True,blank=True,default="The most reliable vendor")
     address=models.CharField(max_length=100,default="1300,O'Block")
     contact=models.CharField(max_length=100,default="+254113708866")
     response_time=models.CharField(max_length=100,default="1")
     shipping_time=models.CharField(max_length=100,default="100")
     rating=models.CharField(max_length=100,default="100")
     return_days=models.CharField(max_length=100,default="100")
     warranty_period=models.CharField(max_length=100,default="100")
     #dlete user model upon vendor delete ?
     user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
     

     class Meta:
        verbose_name_plural="Vendors"

     def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))
    
     def __str__(self):
        return self.title
     
class Tags(models.Model):
    #Not Implimented
    pass
    
class Product(models.Model):
    product_id=ShortUUIDField(unique=True,length=10,max_length=20,prefix="PDT",alphabet="abcdefgh12345")
    title=models.CharField(max_length=100,default="Branded Tshirt")
    image=models.ImageField(upload_to=user_dir_path,default="product.jpg")
    description=models.TextField(null=True,blank=True,default="This is a good product")
    #when user who created pdt deleted , do we delete product
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    price=models.DecimalField(max_digits=999999999999,decimal_places=2,default="10.00")
    standard_price=models.DecimalField(max_digits=999999999999,decimal_places=2,default="5.00")
    specifications=models.TextField(null=True,blank=True)
    #tags=models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)
    product_status=models.CharField(choices=STATUS,max_length=10,default="inreview")
    status=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    featured=models.BooleanField(default=False)
    #for digital products-Allow users pass in address wont show up coz its digital(sent to cust email)
    digital=models.BooleanField(default=False)
    sku=ShortUUIDField(unique=True,length=4,max_length=10,prefix="sku",alphabet="0123456789")
    date=models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural="Products"
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    #calculate discounted prices
    def get_discounted_price(self):
        new_price=(self.price/self.standard_price) * 100
        return new_price

#Allow users to enter multiple product images
class ProductImages(models.Model):
    images=models.ImageField(upload_to='product-images',default="product.jpg")
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Product Images"


################################################## Cart,Order,OrderItems,Address #####################

class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)#Who adds items to cart
    price=models.DecimalField(max_digits=999999999999,decimal_places=2,default="0.00")
    paid_status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=True)
    product_status=models.CharField(choices=STATUS_CHOICE,max_length=30,default="processing")

    class Meta:
        verbose_name_plural="Cart Orders"

#items in cart
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=200)
    product_status=models.CharField(max_length=200)
    item=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    quantity=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=999999999999,decimal_places=2,default="0.00")
    total=models.DecimalField(max_digits=999999999999,decimal_places=2,default="0.00")

    class Meta:
        verbose_name_plural="Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
####################################### Product Review , Wishlist ,Address############################
class ProductReview(models.Model):
    #for each review we have user and review dropped on a single product
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    review=models.TextField()
    rating=models.IntegerField(choices=RATING,default=None)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Product Reviews"

    def __str__(self):
        self.product.title

    def get_rating(self):
        return self.rating
    
class WishList(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="wishlists"

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=100,null=True)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Addresses"