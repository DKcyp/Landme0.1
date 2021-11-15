import os
from os import name
from django.db.models.deletion import SET_NULL
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Permission, auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import item, User, Profile, personaldata
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
# Create your views here.

def index(request):
    user = request.user
    # items = item.objects.all().order_by("-date_created")
    usr = request.user
    src = None
    fav = None
    num = 0
    search_post = request.GET.get('search')
    if search_post == "":
            return redirect('/')
    if search_post:
        src = search_post
        items = item.objects.filter(Q(title__icontains=search_post) | Q(detail__icontains=search_post))
    else:
        items = item.objects.all()
    if user.is_authenticated:
        fav = user.profile.products.all()
        if request.method == "POST":
            item_id = request.POST.get("item_pk")
            product = item.objects.get(id = item_id)
            if product in fav:
                request.user.profile.products.remove(product)
            else:    
                request.user.profile.products.add(product)
            # messages.success(request,(f'{product} added to wishlist.'))
    return render(request, 'index.html', {'item': items, 'usr': usr,'fav':fav,'src':src,'num':num})

def register(request):
    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Use')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Use')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Password Not Same')
            return redirect('register')
    else:
        return render(request, 'register.html',{})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User or Passoword False')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def detail(request, deid):
    items = item.objects.get(id=deid)
    return render(request, 'detail.html',{'deid': deid, 'item':items})

def upload(request):
    if request.user.is_authenticated :
        idn = request.user.id
        usr = request.user.username
        user = User.objects.get(id=idn) 
        usrs = User.objects.get(username=usr)
        if user.personaldata.nowa == None == user.personaldata.nowa:
                return redirect('personal', uss=user.username)
        if request.method == 'POST' :
            title = request.POST['title']
            detail = request.POST['detail']
            harga = request.POST['harga']
            luas = request.POST['luas']
            keunikan = request.POST['keunikan']
            aksesair = request.POST['aksesair']
            sertifikasi = request.POST['sertifikasi']
            lokasi = request.POST['lokasi']
            imgup = request.FILES.get('imgup', False)
            if title !=  "" != detail:
                if imgup:
                    imgup = request.FILES['imgup'] 
                    if item.objects.filter(title=title).exists():
                        messages.info(request, 'Title Already Use')
                        return redirect('upload')
                    else:
                        items = item.objects.create(userid=user, title=title, detail=detail, 
                        images=imgup,harga=harga,lokasi=lokasi,luas=luas,keunikan=keunikan,
                        aksesair=aksesair,sertifikasi=sertifikasi)
                        items.save();
                        return redirect('/')
                else:
                    messages.info(request, 'Must Bee Fill')
                    return redirect('upload')
            else:
                messages.info(request, 'Must Bee Fill')
                return redirect('upload')
        else:
            return render(request, 'add.html' ,{'usr':usrs,'usern':user,'idn':idn})
    else:
        return redirect('/')
def update(request, iid):
    usrs = User.objects.get(username=request.user.username)
    items = item.objects.get(id= iid)
    user = User.objects.get(id=items.userid.id)
    if request.user.id != items.userid.id:
        return redirect('/')
    if request.method == 'POST' :
        title = request.POST['title']
        detail = request.POST['detail']
        harga = request.POST['harga']
        luas = request.POST['luas']
        keunikan = request.POST['keunikan']
        aksesair = request.POST['aksesair']
        sertifikasi = request.POST['sertifikasi']
        lokasi = request.POST['lokasi']
        imgup = request.FILES.get('imgup', False)
        if title !=  "" != detail:
            if imgup:
                imgup = request.FILES['imgup'] 
                items.images = imgup
                items.save
            if items.title != title:
                if item.objects.filter(title=title).exists():
                    messages.info(request, 'Title Already Use')
                    return redirect('update', iid=iid)
            items.title = title
            items.harga = harga
            items.luas = luas
            items.keunikan = keunikan
            items.aksesair = aksesair
            items.sertifikasi = sertifikasi
            items.lokasi = lokasi
            items.detail = detail
            items.save();
            return redirect('userads', usr=usrs)
        else:
            messages.info(request, 'Must Bee Fill')
            return redirect('update', iid=iid)
        
    return render(request, 'editads.html',{'usr':usrs,'iid':iid,'item':items})

def delete(request, item_pk):
    user = request.user.username
    query = item.objects.get(id=item_pk)
    query.delete()
    return redirect('userads', usr=user)

def userprofile(request, usr):
    user = request.user
    usrs = User.objects.get(username=usr)
    search_post = request.GET.get('search')
    if search_post == "":
            return redirect('/')
    if search_post:
        src = search_post
        items = item.objects.filter(Q(title__icontains=search_post,userid = usrs.id) | Q(detail__icontains=search_post,userid = usrs.id))
    else:
        items = item.objects.filter(userid = usrs.id)
    fav = usrs.profile.products.all()
    # usrsx = xo.item_all()
    items = item.objects.filter(userid = usrs.id)
    if user.is_authenticated:
        fav = user.profile.products.all()
        if request.method == "POST":
            item_id = request.POST.get("item_pk")
            product = item.objects.get(id = item_id)
            if product in fav:
                request.user.profile.products.remove(product)
            else:    
                request.user.profile.products.add(product)
    return render(request, 'user.html',{'usr':usrs,'fav':fav,'item':items})
def userads(request, usr):
    usrs = User.objects.get(username=usr)
    items = item.objects.filter(userid = usrs.id)

    return render(request, 'ads.html',{'usr':usrs,'item':items})
def dashboard(request, usr):
    usrs = User.objects.get(username=usr)
    fav = usrs.profile.products.all()
    # usrsx = xo.item_all()
    items = item.objects.filter(userid = usrs.id)
    if request.user.username != usrs.username or request.user.username == None:
        return redirect('/')
    if request.method == "POST":
        pass
    return render(request, 'dashboard.html',{'usr':usrs,'fav':fav,'item':items})

def personal(request, uss):
    user = User.objects.get(username = uss)
    data = personaldata.objects.get(user = user.id)
    if request.method == 'POST' :
        phonenum = request.POST['phonenum']
        nowa = request.POST['nowa']
        address = request.POST['address']
        pob = request.POST['pob']
        dob = request.POST['dob']
        gender = request.POST.get("gender", None)
        if phonenum != "" != nowa and address != "" != pob and dob != "":
            if gender in ["Male", "Female"] :
                data.gender = gender
                data.save()
            else:
                data.gender = None
                data.save()
            data.phonenum = phonenum
            data.nowa = nowa
            data.address = address
            data.pob = pob
            data.dob = dob
            data.save()
            return redirect('personal', uss=user.username)
        else:    
            messages.info(request, 'Must Bee Fill')
            return redirect('upload')
    return render(request, 'personal.html', {'usr':user})

def profilesetting(request, uss):
    # user = request.user
    user = User.objects.get(username = uss)
    profile = Profile.objects.get(user = user.id)
    if request.method == 'POST' :
        usernamex = request.POST['username']
        fullname = request.POST['fullname']
        headline = request.POST['headline']
        bio = request.POST['bio']
        profilepic = request.FILES.get('profilepic', False)
        if usernamex != "" != fullname and headline != "" != bio:
            if user.username != usernamex:
                if User.objects.filter(username=usernamex).exists():
                        messages.info(request, 'Username Already Use')
                        return redirect('profilesetting', uss=uss)
            if profilepic:
                profilepic = request.FILES['profilepic']
                profile.userpic = profilepic
                profile.save()
            else:
                messages.info(request, 'Must Bee Fill')
                return redirect('profilesetting', uss=user.username)
            user.username = usernamex
            profile.fullname = fullname
            profile.headline = headline
            profile.bio = bio
            profile.save()
            user.save()
            return redirect('profilesetting', uss=user.username)
        else:
            messages.info(request, 'Must Bee Fill')
            return redirect('profilesetting', uss=user.username)
    else:
        return render(request, 'profile.html', {'usr':user})
def account(request, uss):
    user = User.objects.get(username = uss)
    profile = Profile.objects.get(user = user.id)
    if request.method == 'POST' :
        if 'email' in request.POST:
            email = request.POST['email']
            user.email = email
            user.save()
        if 'password' in request.POST:
            newpassword = request.POST['newpassword']
            repassword = request.POST['repassword']
            if newpassword == repassword :
                user.set_password(newpassword)
                user.save()
                return redirect('/login')
            else :
                messages.info(request, 'Not Same')
                return redirect('account', uss=user)
    return render(request, 'account.html', {'usr':user})
def about(request):
    if request.user.is_authenticated :
        usrs = User.objects.get(username=request.user.username)
        return render(request, 'about.html',{'usr':usrs})
    else:
        usrs = None
        return render(request, 'about.html',{'usr':usrs})
def contact(request):
    if request.user.is_authenticated :
        usrs = User.objects.get(username=request.user.username)
        return render(request, 'contact.html',{'usr':usrs})
    else:
        usrs = None
        return render(request, 'contact.html',{'usr':usrs})
def bookmark(request, usr):
    user = request.user.username
    if user != usr:
        return redirect('bookmark', usr=user)
    usrs = User.objects.get(username=usr)
    search_post = request.GET.get('search')
    src = None
    if search_post == "":
            return redirect('/')
    if search_post:
        src = search_post
        fav = usrs.profile.products.objects.filter(Q(title__icontains=search_post) | Q(detail__icontains=search_post))
    else:
        fav = usrs.profile.products.all()
    fav = usrs.profile.products.all()
    if request.user.is_authenticated:
        fav = request.user.profile.products.all()
        if request.method == "POST":
            item_id = request.POST.get("item_pk")
            product = item.objects.get(id = item_id)
            if product in fav:
                request.user.profile.products.remove(product)
            else:    
                request.user.profile.products.add(product)
    return render(request, 'bookmark.html',{'usr':usrs,'item':fav,'src':src})
# def profilesetting(request, uss):
#     # user = request.user
#     user = User.objects.get(username = uss)
#     profile = Profile.objects.get(user = user.id)
#     if request.method == 'POST' :
#         usernamex = request.POST['username']
#         emailx = request.POST['email']
#         bio = request.POST['bio']
#         alamat = request.POST['alamat']
#         notelp = request.POST['notelp']
#         profilepic = request.FILES.get('profilepic', False)
#         if user.username != usernamex:
#             if User.objects.filter(username=usernamex).exists():
#                     messages.info(request, 'Username Already Use')
#                     return redirect('profilesetting', uss=uss)
#         if user.email != emailx:
#             if User.objects.filter(email=emailx).exists():
#                 messages.info(request, 'Email Already Use')
#                 return redirect('profilesetting', uss=uss)
#         if profilepic:
#             profilepic = request.FILES['profilepic']
#             profile.userpic = profilepic
#             profile.save()
#         user.username = usernamex
#         user.email = emailx
#         profile.bio = bio
#         profile.alamat = alamat
#         profile.notelp = notelp
#         user.save()
#         profile.save()
#         return redirect('profile', usr=user.username)
#     else:
#         return render(request, 'profilesetting.html')
    

