from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from django.contrib import messages
from shoppingapp.models import Product,userdetails,Cart,Category
from django.http import HttpResponse
def ho(request):
    cat=Category.objects.all()
    return render(request,'home.html',{'ca':cat})
def log(request):
    return render(request,'login.html')
def sign(request):
    return render(request,'signup.html')
def adm(request):
    return render(request,'admin.html')
def use(request):
    return render(request,'user.html')
def hlog(request):
    if request.method=='POST':
        lname=request.POST['lna']
        lpss=request.POST['lpas']
        lo=auth.authenticate(username=lname,password=lpss)
        if lo is not None:
            if lo.is_staff:
                login(request,lo)
                return redirect('adm')
            else:
                login(request,lo)
                auth.login(request,lo)
                return redirect('us_home')
def add_usr(request):
    if request.method=='POST':
        tfname=request.POST['tfna']
        tlname=request.POST['tlna']
        tuname=request.POST['tuna']
        tpassword=request.POST['tpass']
        tcpassword=request.POST['tcpass']
        taddress=request.POST['tadd']
        tcontact=request.POST['tcon']
        tmail=request.POST['tema']
        timage=request.FILES['timg']
        if tpassword==tcpassword:
            if User.objects.filter(username=tuname).exists():
                messages.info(request,'This user name already exists....')
                return redirect('ho')
            else:
                us=User.objects.create_user(
                    first_name=tfname,
                    last_name=tlname,
                    username=tuname,
                    email=tmail,
                    password=tpassword
                )
                us.save()
        else:
            messages.info(request,'Password does not match...')
            return redirect('add_usr')
        teac=userdetails(address=taddress,number=tcontact,usimg=timage,user=us)
        teac.save()
        return redirect('ho')
def cate(request):
    return render(request,'add_category.html')
def adcate(request):
    if request.method=='POST':
        cname=request.POST['cna']
        cn=Category(category_Name=cname)
        cn.save()
        return redirect('adm')
def prod(request):
    cor=Category.objects.all()
    return render(request,'add_products.html',{'co':cor})
def adpro(request):
    if request.method=='POST':
        pname=request.POST['prn']
        prdes=request.POST['prd']
        price=request.POST['pri']
        pimage=request.FILES['ima']
        popt=request.POST['se']
        op=Category.objects.get(id=popt)
        pr=Product(prname=pname,prprice=price,prdesc=prdes,primg=pimage,category=op)
        pr.save()
        return redirect('show_prod')

def show_prod(request):
    shpr=Product.objects.all()
    return render(request,'product_details.html',{'pr':shpr})
def show_users(request):
    susrs=userdetails.objects.all()
    return render(request,'user_details.html',{'su':susrs})

def test(request):
    cor=Category.objects.all()
    return render(request,'test.html',{'co':cor})
def men(request):
    return render(request,'men.html')
def women(request):
    return render(request,'women.html')
def us_home(request):
    cur_user=request.user.id
    user1=userdetails.objects.get(user_id=cur_user)
    cato=Category.objects.all()
    return render(request,'user_home.html',{'su':user1,'ca':cato})
def prolist(request,k):
    catr=Category.objects.get(id=k)
    prods=Product.objects.filter(category=catr)
    return render(request,'pro_list.html',{'cat':catr,'pro':prods})
def pro_list(request):
    return render(request,'pro_list.html')
def cart(request,k):
    pr=Product.objects.get(id=k)
    cart_item, created=Cart.objects.get_or_create(user=request.user,prod=pr)
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('cartde')
def logout(request):
    auth.logout(request)
    return redirect('ho')    
def deletepro(request,k):
    tea=Product.objects.get(category=k)
    use=Category.objects.get(id=k)
    tea.delete()
    use.delete()
    return redirect('show_prod')
def deleteusr(request,k):
    tea=userdetails.objects.get(user=k)
    use=User.objects.get(id=k)
    tea.delete()
    use.delete()
    return redirect('show_users')
def cartde(request):
    cart_items=Cart.objects.filter(user=request.user).select_related('prod')
    total_pr=sum(item.total_price() for item in cart_items)
    return render(request,'cart.html',{'caite':cart_items,'totalpr':total_pr})
def increase(request,k):
    cart_item=Cart.objects.get(prod_id=k,user=request.user)
    cart_item.quantity +=1
    cart_item.save()
    return redirect('cartde')
def decrease(request,k):
    cart_item=Cart.objects.get(prod_id=k,user=request.user)
    cart_item.quantity -=1
    cart_item.save()
    return redirect('cartde')
def remove(request,k):
    cart_item=Cart.objects.filter(user=request.user).first()
    if cart_item:
        cart_item.delete()
    return redirect('cartde')
def cart1(request):
    return render(request,'cart.html')



    
