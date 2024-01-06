from django.shortcuts import render,redirect
from .forms import *
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
# Create your views here.

class stafflogin(View):
    def get(self,request):
        return render(request,'login.html',{'form':LoginForm()})
    def post(self,request):
        loginVal=LoginForm(request.POST)
        if loginVal.is_valid():
            username=loginVal.cleaned_data['username']
            password=loginVal.cleaned_data['password']
            getUser=authenticate(username=username,password=password)
            if getUser is not None:
                if getUser.is_staff:
                    login(request,getUser)
                    return redirect('storeadmin:storepanel')
                loginVal.add_error('username','user is not staff')
        loginVal.add_error(None,'Error username or password')
        return render(request,'login.html',{'form':loginVal})
class staffLogout(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect('storeadmin:stafflogin')
        else:
            logout(request)
            return redirect('storeadmin:stafflogin')
@method_decorator(login_required(login_url='storeadmin:stafflogin'),name="dispatch")
class StoreAdminPanel(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        return render(request,'storeadmin/storeadmin.html')   
@method_decorator(login_required(login_url='storeadmin:stafflogin'),name="dispatch")
class AddBookView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        return render(request,'storeadmin/addbook.html',{'form':BookCreationForm()})
    def post(self,request):
        book=BookCreationForm(request.POST,request.FILES)
        if book.is_valid():
            book.save()
        else:
            book.add_error(None,"Book creation error")
        print(book.errors)
        return render(request,'storeadmin/addbook.html',{'form':book})
@method_decorator(login_required(login_url='storeadmin:stafflogin'),name="dispatch")
class AddAuthor(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        return render(request,'storeadmin/addauthor.html',{'form':AuthorCreation()})
    def post(self,request):
        author=AuthorCreation(request.POST)
        if author.is_valid():
            author.save()
            return redirect('storeadmin:addbook')
        else:
            author.add_error(None,"Author creation error")
        return render(request,'storeadmin/addauthor.html',{'form':author})
@method_decorator(login_required(login_url='storeadmin:stafflogin'),name="dispatch")
class AddGenre(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        return render(request,'storeadmin/addgenre.html',{'form':GenreCreation()})
    def post(self,request):
        genre=GenreCreation(request.POST)
        if genre.is_valid():
            genre.save()
            return redirect('storeadmin:addbook')
        else:
            genre.add_error(None,"Author creation error")
        return render(request,'storeadmin/addgenre.html',{'form':genre})
