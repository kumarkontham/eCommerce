from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from cartapp.models import Product,Cartitem,Contact,ShippingAddress
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.conf import settings
from .forms import ShippingForm,AddressupdateForm
from django.views.decorators.http import require_POST
from decimal import Decimal
def Signup_view(request):
    if request.method=='POST':
        username=request.POST['email']
        email=request.POST['email']
        password=request.POST['p1']
        confirm=request.POST['p2']
        print(email)
        if password != confirm:
            messages.warning(request,"Password not matching")
            return render(request,"signup.html")
        try :
            if User.objects.get(username=email):
                messages.warning(request,"Email already exist")
                return render(request,"signup.html")
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,username,password)
        user.save()
        messages.success(request,"Details added successfully..")
    return render(request,'signup.html')
def Login_view(request):
    if request.method=="POST":
        email=request.POST['un']
        pass1=request.POST['p1']
        myuser=authenticate(username=email ,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect("/")
        else:
            messages.warning(request,"Invalid username or Password")
            return render(request,"login.html")
    return render(request,'login.html')
def logout_view(request):
    logout(request)
    
    return redirect("/login/")
def log_view(request):
    return render(request,"log.html")

def Contact_view(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        desc=request.POST['desc']
        phone=request.POST['pn']
        req=Contact(name=name,email=email,desc=desc,phone=phone)
        req.save()
        messages.success(request,"we will get back you soon!")
        return redirect("/contact/")
    return render(request,"contact.html")
def base_view(request):
    products = Product.objects.all()
    return render(request, 'base.html', {'products': products})
    
def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})
def view_cart(request):
    cart_items=Cartitem.objects.filter(user=request.user)
    amount=0
    shipping=0
    totalamount=0
    value=0
    
    
    for p in cart_items:
        if p.quantity>=1:
            shipping=40
            value=p.quantity*p.product.price
            amount=amount+value
            totalamount=amount+shipping
            
            
            
    
            
        else:
            shipping=0
            value=p.quantity*p.product.price
            amount=amount+value
            totalamount=amount

    
    return render(request,'cart.html',{"cart_items":cart_items,"amount":amount,"totalamount":totalamount,"shipping":shipping,"value":value})

def add_to_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    cart_item,created=Cartitem.objects.get_or_create(product=product,user=request.user)
    if cart_item.quantity>=2:
        messages.warning(request,"This product cart limit is over...")
    else:
        cart_item.quantity += 1
        totalp=product.price *cart_item.quantity
        print("product total price: ",totalp)
    

        if cart_item.quantity>=1:
            shipping=40
        else:
            shipping=0
        cart_item.save()
        messages.success(request,"item added to cart successfully!...")
        redirect_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(product_list)
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cartitem.objects.get(Q(product=prod_id)&Q(user=request.user))
        if c.quantity>=2:
            messages.warning(request,"once limited products only purchase")
        else:
            c.quantity+=1

        c.product.price=c.quantity*c.product.price
        
        c.save()
        
        user=request.user
        cart=Cartitem.objects.filter(user=user)
        amount=0
        
        for p in cart:
            shipping=40
            value=p.quantity*p.product.price
            amount=amount+value
            if amount>1:
                totalamount=amount+shipping
            elif amount<1 and amount==0:
                shipping=0
                totalamount=amount
            data={
                "sub_total":c.product.price,
                "quantity":c.quantity,
                "amount":amount,
                "shipping":shipping,
                "totalamount":totalamount,

        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cartitem.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        sub_total=c.quantity*c.product.price
        c.save()
        user=request.user
        cart=Cartitem.objects.filter(user=user)
        amount=0
        for p in cart:
            
            value=p.quantity*p.product.price
            amount=amount+value
            if amount>=1:
                shipping=40
                totalamount=amount+shipping
            elif amount<1 and amount==0:
                shipping=0
                totalamount=amount
            data={
            "sub_total":sub_total,
            "quantity":c.quantity,
            "amount":amount,
            "shipping":shipping,
            "totalamount":totalamount,

        }
        return JsonResponse(data)
    
def remove(request,id):
    cart=Cartitem.objects.get(id=id)
    cart.delete()
    return redirect(view_cart)
def product_search(request):
    query = request.GET.get('query', '')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
        products = Product.objects.filter(name__icontains=query) if query else []
        data = [{'image_url':product.image.url if product.image.url else '' , 'name': product.name, 'price': str(product.price)} for product in products]
        return JsonResponse({'products': data})

    return render(request, '/search') 
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.filter(Q(name__icontains=keyword)|Q(description__icontains=keyword))
            count=products.count()
        
    return render(request,'search.html',{'products':products,'count':count})
def checkout_view(request):
    cart_items=Cartitem.objects.filter(user=request.user)
    shad=ShippingAddress.objects.filter(user=request.user)
    amount=0
    shipping=0
    totalamount=0
    value=0
    
    
    for p in cart_items:
        if p.quantity>=1:
            shipping=40
            value=p.quantity*p.product.price
            amount=amount+value
            totalamount=amount+shipping  
        else:
            shipping=0
            value=p.quantity*p.product.price
            amount=amount+value
            totalamount=amount
    shipping_form = ShippingForm()
    
    if request.method == "POST":
        
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            return redirect("checkout_view")
    

    
    return render(request,'checkout.html',{"cart_items":cart_items,"amount":amount,"totalamount":totalamount,"shipping":shipping,"value":value,"form": shipping_form,"shad":shad})
    
def delete_add(request,id):
    s=ShippingAddress.objects.get(id=id)
    s.delete()
    id=id-1
    messages.warning(request,"Address delated successfully!")
    return redirect(checkout_view)
def Update_add(request,id):
    address=ShippingAddress.objects.get(id=id,user=request.user)
    if request.method=="POST":
        form=AddressupdateForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated shipping Address Successfully!")
            return redirect(checkout_view)
    else:
        form = AddressupdateForm(instance=address)
    return render(request,'updateadd.html',{"form":form,"address":address})
def category_view(request,category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'category.html', {
        'products': products,
        'selected_category': category_name,
    })
def product_detailed_view(request,product_id):
    product=Product.objects.get(id=product_id)
    return render(request,'product_view.html',{'product':product})


    



# Create your views here.
