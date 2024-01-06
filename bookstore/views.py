from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
# Create your views here.
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class Home(View):
    def get(self,request):
        genre_id = request.GET.get('genre')
        book_val=request.GET.get('searckBook')
        if genre_id is None and book_val is None:
            books=Book.objects.all()
        elif genre_id is not None:
            books = Book.objects.filter(genre_id=genre_id)
        else:
            books = Book.objects.filter(title__icontains=book_val)
        genre=Genre.objects.all()
        return render(request,'bookstore/home.html',{'books':books,'genre':genre,'messages':''})
    def post(self,request):
        book_id=request.POST.get('book_id')
        try:
            check_cart=Cart.objects.get(user=request.user, items__id=book_id)
            if check_cart is not None:
                check_cart.quantity+=1
                check_cart.save()
                messages='Cart incremented successfully.'
            else:
                new_cart=Cart.objects.create(user=request.user, items_id=book_id)
                new_cart.save()
                messages='New item added to the cart.'
        except:
            new_cart=Cart.objects.create(user=request.user, items_id=book_id)
            new_cart.save()
            messages='New item added to the cart.'
        books=Book.objects.all()
        genre=Genre.objects.all()
        return render(request,'bookstore/home.html',{'books':books,'genre':genre,'messages':messages})
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{'form':LoginForm()})
    def post(self,request):
        loginVal=LoginForm(request.POST)
        if loginVal.is_valid():
            email=loginVal.cleaned_data['email']
            password=loginVal.cleaned_data['password']
            getUser=authenticate(email=email,password=password)
            if getUser is not None:
                secret_key = pyotp.random_base32()
                motp=pyotp.TOTP(secret_key)
                otp=motp.now()
                request.session['otp']=otp
                request.session['otp_user']=getUser.id
                send_mail("OTP Number",f"Your OTP is {otp}",settings.EMAIL_HOST_USER,[email])
                return redirect("bookstore:otpverify")
        loginVal.add_error(None,'Error Email or password')
        return render(request,'login.html',{'form':loginVal})
class OTPVerification(View):
    def get(self,request):
        return render(request,'bookstore/otpverify.html',{'form':OTPform})
    def post(self,request):
        otpform=OTPform(request.POST)
        if otpform.is_valid():
            otp=otpform.cleaned_data['otpvalue']
            otp_in_session=request.session.get('otp')
            otp_user=request.session.get('otp_user')
            if otp_user is None:
                return redirect('bookstore:login')
            if otp==otp_in_session:
                user = User.objects.get(id=otp_user)
                if user is not None:
                    login(request,user,backend='bookstore.customauth.EmailBackend')
                    del request.session['otp']
                    del request.session['otp_user']
                    return redirect('bookstore:home')
        print(otpform.errors)
        return render(request,'bookstore/otpverify.html',{'form':otpform,'error':'OTP verification failed'})
class RegisterView(View):
    def get(self,request):
        return render(request,'bookstore/register.html',{'form':RegisterForm})
    def post(self,request):
        register_user=RegisterForm(request.POST)
        if register_user.is_valid():
            register_user.save()
            return redirect('bookstore:login')
        return render(request,'bookstore/register.html',{'form':register_user})
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('bookstore:login')
class ConfirmEmail(View):
    def get(self,request,token):
        user_match=get_object_or_404(EmailTokenGeneration,token=token)
        user=user_match.user
        if user.is_active:
            return HttpResponse("Your email has already been confirmed.")
        else:
            user.is_active=True
            user.save()
            return render(request,'bookstore/email_sucess.html')
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class BookDetail(View):
    def get(self,request,book_id):
        book=Book.objects.get(id=book_id)
        comments=Comment.objects.filter(book=book_id)
        return render(request,'bookstore/bookdetail.html',{'book':book,'comments':comments})
    def post(self,request,book_id):
        comment_value=request.POST.get('comment')
        book=Book.objects.get(id=book_id)
        comment_creation=Comment.objects.create(value=comment_value,comment_user=request.user,book=book)
        comment_creation.save()
        comments=Comment.objects.filter(book=book_id)
        return render(request,'bookstore/bookdetail.html',{'book':book,'comments':comments})
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class CartView(View):
    def get(self,request):
        cart_items=Cart.objects.filter(user=request.user)
        cart_items_dict = {}
        for cart_item in cart_items:
            book_values = {
                "title": cart_item.items.title,  
                "price": cart_item.items.price,
                "book_image": cart_item.items.book_image.url,
                "quantity": cart_item.quantity,
            }
            cart_items_dict[cart_item.id] = book_values
        return render(request,'bookstore/cart.html',{'cart':cart_items_dict})
    def post(self,request):
        cart_items=Cart.objects.filter(user=request.user)
        book_ordered=""
        coupon=request.POST.get('coupon')
        if coupon is None:
            coupon="None"
        for cart_item in cart_items:
            cart_history_check=CartHistory.objects.filter(items=cart_item.items)
            print(cart_history_check)
            if cart_history_check:
                cart_history_check[0].quantity+=cart_item.quantity
                cart_history_check[0].save()
            else:
                cart_history=CartHistory.objects.create(user=request.user,items=cart_item.items,quantity=cart_item.quantity)
                cart_history.save()
            title=cart_item.items.title
            quantity=cart_item.quantity
            price=cart_item.items.price*quantity
            book_ordered+=f"Name:{title} Quantity:{quantity} Price:{price}\n"
        book_ordered+=f"coupon:{coupon}"
        subject="Book Ordered"
        send_mail(subject,book_ordered,settings.EMAIL_HOST_USER,[request.user.email])
        cart_items.delete()
        return render(request,'bookstore/cart.html',{'cart':'','msg':"Ordered placed sucessfully! Cart cleared"})
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class History(View):
    def get(self,request):
        cart_items=CartHistory.objects.filter(user=request.user)
        cart_items_dict = {}
        for cart_item in cart_items:
            book_values = {
                "title": cart_item.items.title,  
                "price": cart_item.items.price,
                "book_image": cart_item.items.book_image.url,
                "quantity": cart_item.quantity,
            }
            cart_items_dict[cart_item.id] = book_values
        return render(request,'bookstore/history_cart.html',{'cart':cart_items_dict})
@method_decorator(login_required(login_url='bookstore:login'),name="dispatch")
class WishlistView(View):
    def get(self,request):
        wishlist = Wishlist.objects.filter(wish_user=request.user)
        books = wishlist.values_list('books', flat=True)
        book_values = Book.objects.filter(pk__in=books)
        
        context = {
            'books': book_values
        }
        return render(request,'bookstore/wishlist.html',context)
    def post(self,request):
        book_id=request.POST.get('book')
        book=Book.objects.get(id=book_id)
        wishlist_obj=Wishlist.objects.create(wish_user=request.user)
        wishlist_obj.books.set([book])
        wishlist_obj.save()
        msg=f"Book:{book.title} added to wishlist"
        return JsonResponse({'msg':msg})