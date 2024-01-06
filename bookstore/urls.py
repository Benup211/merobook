from django.urls import path
from .views import *
app_name='bookstore'
urlpatterns=[
    path('',Home.as_view(),name="home"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('cart/',CartView.as_view(),name="cart"),
    path('history/',History.as_view(),name="history"),
    path('register/',RegisterView.as_view(),name="register"),
    path('confirm-email/<str:token>/',ConfirmEmail.as_view(),name="confirm"),
    path('login/otpcode/',OTPVerification.as_view(),name="otpverify"),
    path('bookdetail/<int:book_id>/',BookDetail.as_view(),name="bookdetail"),
    path('wishlist/',WishlistView.as_view(),name="wishlist"),
]