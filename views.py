from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random
import uuid

def index(request):
    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html',d)



def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    ccount = Criminal.objects.all().count()
    pcount = Police.objects.all().count()
    catcount = Category.objects.all().count()
    pscount = PoliceStation.objects.all().count()
    d = {'ccount': ccount,'pcount': pcount,'catcount': catcount,'pscount': pscount}
    return render(request, 'admin_home.html',d)


def add_policestation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        psn = request.POST['policestationname']
        psc = request.POST['policestationcode']
        try:
            PoliceStation.objects.create(policestationname=psn,policestationcode=psc,creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_policestation.html', d)


def manage_policestation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    station = PoliceStation.objects.all()
    d = {'station':station}
    return render(request, 'manage_policestation.html', d)

def edit_policestation(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    station = PoliceStation.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        psn = request.POST['policestationname']
        psc = request.POST['policestationcode']
        station.policestationname = psn
        station.policestationcode = psc
        try:
            station.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'station':station}
    return render(request, 'edit_policestation.html',d)

def delete_policestation(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    station = PoliceStation.objects.get(id=pid)
    station.delete()
    return redirect('manage_policestation')


def add_police(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    station = PoliceStation.objects.all()
    error = ""
    if request.method=="POST":
        ps = request.POST['policestation']
        pid = request.POST['pid']
        pn = request.POST['name']
        pe = request.POST['email']
        pm = request.POST['mobnum']
        paddr = request.POST['address']
        ppwd = request.POST['password']
        stationid = PoliceStation.objects.get(id=ps)
        try:
            user = User.objects.create_user(first_name=pn,last_name=pm,username=pe,password=ppwd)
            Police.objects.create(user=user,policestationid=stationid,pid=pid,address=paddr,joiningdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'station':station}
    return render(request, 'add_police.html', d)


def manage_police(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    police = Police.objects.all()
    d = {'police':police}
    return render(request, 'manage_police.html', d)


def edit_police(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    station = PoliceStation.objects.all()
    police = Police.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        ps = request.POST['policestation']
        pid = request.POST['pid']
        pn = request.POST['name']
        pe = request.POST['email']
        pm = request.POST['mobnum']
        paddr = request.POST['address']
        stationid = PoliceStation.objects.get(id=ps)
        police.policestationid = stationid
        police.pid = pid
        user1 = User.objects.get(id=police.user.id)
        user1.first_name = pn
        user1.last_name = pm
        police.address = paddr
        try:
            police.save()
            user1.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'station':station,'police':police}
    return render(request, 'edit_police.html',d)


def delete_police(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('manage_police')


def add_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        psn = request.POST['catname']
        psc = request.POST['catdes']
        try:
            Category.objects.create(catname=psn,catdes=psc)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_category.html', d)


def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    d = {'category':category}
    return render(request, 'manage_category.html', d)

def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        cn = request.POST['catname']
        cd = request.POST['catdes']
        category.catname = cn
        category.catdes = cd
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'category':category}
    return render(request, 'edit_category.html',d)


def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manage_category')


def Logout(request):
    logout(request)
    return redirect('index')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_passwordadmin.html',d)


def police_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'police_login.html', d)


def police_home(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid,status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    approvedfircount = Fir.objects.filter(policestationid=policeid.policestationid, status="Approved").count()
    rejectedfircount = Fir.objects.filter(policestationid=policeid.policestationid, status="Cancelled").count()
    newchargesheetcount = Fir.objects.filter(policestationid=policeid.policestationid, status="Approved").count()
    comchargesheetcount = Fir.objects.filter(policestationid=policeid.policestationid, status="Charge Sheet Completed").count()
    criminalcount = Criminal.objects.filter(policeid=policeid).count()
    d = {'newfircount':newfircount,'approvedfircount':approvedfircount,'rejectedfircount':rejectedfircount,'newchargesheetcount':newchargesheetcount,'comchargesheetcount':comchargesheetcount,'criminalcount':criminalcount,'newfir':newfir}
    return render(request, 'police_home.html',d)


def add_criminal(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    category = Category.objects.all()
    station = PoliceStation.objects.all()
    error = ""
    if request.method=="POST":
        psn = request.POST['policestation']
        ctype = request.POST['crimetype']
        cd = request.POST['cdate']
        ct = request.POST['ctime']
        prison = request.POST['prison']
        court = request.POST['court']
        name = request.POST['name']
        contact = request.POST['connum']
        height = request.POST['height']
        weight = request.POST['weight']
        dob = request.POST['dob']
        email = request.POST['email']
        addr = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip = request.POST['zipcode']
        photo = request.FILES['cphoto']
        userid = User.objects.get(id=request.user.id)
        policeid = Police.objects.get(user=userid)
        stationid = PoliceStation.objects.get(id=psn)
        categoryid = Category.objects.get(id=ctype)
        cid = str(random.randint(10000000, 99999999))
        try:
            Criminal.objects.create(criminalid=cid,policeid=policeid,policestationid=stationid,catname=categoryid,crimedate=cd,crimetime=ct,prison=prison,court=court,name=name,contactno=contact,height=height,weight=weight,dob=dob,email=email,address=addr,city=city,state=state,country=country,zipcode=zip,photo=photo,recorddate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category,'station':station,'newfir':newfir,'newfircount':newfircount}
    return render(request, 'add_criminal.html', d)


def manage_criminal(request):
    if not request.user.is_authenticated:
        return redirect('police_login')

    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    criminal = Criminal.objects.filter(policeid=policeid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    d = {'criminal':criminal,'newfir':newfir,'newfircount':newfircount}
    return render(request, 'manage_criminal.html', d)


def edit_criminal(request,pid):
    if not request.user.is_authenticated:
        return redirect('police_login')
    criminal = Criminal.objects.get(id=pid)
    category = Category.objects.all()
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    error = ""
    if request.method=="POST":
        ctype = request.POST['crimetype']
        cd = request.POST['cdate']
        ct = request.POST['ctime']
        prison = request.POST['prison']
        court = request.POST['court']
        name = request.POST['name']
        contact = request.POST['connum']
        height = request.POST['height']
        weight = request.POST['weight']
        dob = request.POST['dob']
        email = request.POST['email']
        addr = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip = request.POST['zipcode']
        categoryid = Category.objects.get(id=ctype)
        criminal.catname = categoryid


        criminal.prison = prison
        criminal.court = court
        criminal.name = name
        criminal.contactno = contact
        criminal.height = height
        criminal.weight = weight
        criminal.email = email
        criminal.address = addr
        criminal.city = city
        criminal.state = state
        criminal.country = country
        criminal.zipcode = zip
        try:
            criminal.save()
            error = "no"
        except:
            error = "yes"
        if cd:
            try:
                criminal.crimedate = cd
                criminal.save()
            except:
                pass
        else:
            pass
        if ct:
            try:
                criminal.crimetime = ct
                criminal.save()
            except:
                pass
        else:
            pass
        if dob:
            try:
                criminal.dob = dob
                criminal.save()
            except:
                pass
        else:
            pass
    d = {'error':error,'category':category,'criminal':criminal,'newfir':newfir,'newfircount':newfircount}
    return render(request, 'edit_criminal.html', d)


def change_image(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    criminal = Criminal.objects.get(id=pid)
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    error = ""
    if request.method=="POST":
        try:
            i = request.FILES['newpic']
            criminal.photo = i
            criminal.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'criminal':criminal,'newfir':newfir,'newfircount':newfircount}
    return render(request, 'change_image.html', d)


def delete_criminal(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    criminal = Criminal.objects.get(id=pid)
    criminal.delete()
    return redirect('manage_criminal')


def change_passwordpolice(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error,'newfir':newfir,'newfircount':newfircount}
    return render(request,'change_passwordpolice.html',d)


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u, password=p)

        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"

    d = {'error': error}
    return render(request, 'user_login.html', d)


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status = 'Accepted',userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    d = {'firuser': firuser,'firusercount':firusercount}
    return render(request, 'user_home.html',d)


def user_signup(request):
    error = ""
    if request.method=="POST":
        fn = request.POST['fname']
        em = request.POST['email']
        mn = request.POST['mobno']
        pwd = request.POST['password']
        try:
            User.objects.create_user(first_name=fn, last_name=mn, username=em, password=pwd)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'user_signup.html', d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error,'firuser':firuser,'firusercount':firusercount}
    return render(request,'change_passworduser.html',d)

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    user=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        f = request.POST['name']
        m = request.POST['mobilenumber']
        user.first_name=f
        user.last_name=m
        try:
            user.save()
            error = "no"
        except:
            error="yes"
    d = {'error':error,'firuser':firuser,'firusercount':firusercount}
    return render(request, 'user_profile.html',d)


def fir_form(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    category = Category.objects.all()
    station = PoliceStation.objects.all()
    error = ""
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    if request.method=="POST":
        psn = request.POST['policestation']
        ctype = request.POST['crimetype']
        nofacc = request.POST['nofaccused']
        parentage = request.POST['parentage']
        name = request.POST['name']
        contact = request.POST['connum']
        addr = request.POST['address']
        relacc = request.POST['relaccused']
        purpose = request.POST['purpose']

        uuid.uuid4().hex

        userid = User.objects.get(id=request.user.id)
        stationid = PoliceStation.objects.get(id=psn)
        categoryid = Category.objects.get(id=ctype)
        firno = uuid.uuid4().hex
            #str(random.randint(10000000, 99999999))
        try:
            Fir.objects.create(firno=firno,userid=userid,policestationid=stationid,crimetype=categoryid,nameaccused=nofacc,nameapplicants=name,parentageapplicant=parentage,contactno=contact,address=addr,relationaccused=relacc,purposeoffir=purpose,dateoffir=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category,'station':station,'firuser': firuser,'firusercount':firusercount}
    return render(request, 'fir_form.html', d)


def police_profile(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    error = ""
    user=User.objects.get(id=request.user.id)
    police = Police.objects.get(user=user)
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    if request.method == 'POST':
        n = request.POST['name']
        mn = request.POST['mobilenumber']
        addr = request.POST['add']
        user.first_name=n
        user.last_name=mn
        police.address = addr
        try:
            police.save()
            user.save()
            error = "no"
        except:
            error="yes"
    d = {'error':error,'police':police,'newfir':newfir,'newfircount':newfircount}
    return render(request, 'police_profile.html',d)


def new_fir(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid,status=None)
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'new_fir.html', d)

def fir_history(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    userid = User.objects.get(id=request.user.id)
    fir = Fir.objects.filter(~Q(status = 'Charge Sheet Completed'),userid=userid)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    d = {'fir':fir,'firuser': firuser,'firusercount':firusercount}
    return render(request,'fir_history.html', d)

def view_firdetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    fir = Fir.objects.get(id=pid)
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    d = {'fir':fir,'firuser': firuser,'firusercount':firusercount}
    return render(request,'view_firdetails.html',d)

def fir_details(request,pid):
    if not request.user.is_authenticated:
        return redirect('police_login')
    fir = Fir.objects.get(id=pid)
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    error = ""
    if request.method == 'POST':
        rem = request.POST['remark']
        status = request.POST['status']
        fir.status = status
        fir.remark = rem
        fir.remarkdate = date.today()
        try:
            fir.save()
            error = "no"
        except:
            error = "yes"
    d = {'fir':fir,'error':error,'newfir':newfir,'newfircount':newfircount}
    return render(request,'fir_details.html',d)

def approved_fir(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid,status="Approved")
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'approved_fir.html', d)

def cancelled_fir(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid,status="Cancelled")
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'cancelled_fir.html',d)

def all_fir(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid)
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'all_fir.html',d)

def new_chargesheet(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid,status="Approved")
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'new_chargesheet.html',d)


def fill_chargesheetdetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('police_login')
    fir = Fir.objects.get(id=pid)
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    error = ""
    if request.method == 'POST':
        sol = request.POST['sol']
        noio = request.POST['noio']
        invdetail = request.POST['invdetail']
        remark = request.POST['remark']
        status = request.POST['status']
        fir.sectionoflaw = sol
        fir.investigationofficer = noio
        fir.investigationdetail = invdetail
        fir.chargesheetdate = date.today()
        fir.remarkdate = date.today()
        fir.remark = remark
        fir.status = status
        try:
            fir.save()
            error = "no"
        except:
            error = "yes"
    d = {'fir':fir,'error':error,'newfir':newfir,'newfircount':newfircount}
    return render(request,'fill_chargesheetdetails.html',d)

def betweendates_criminalreport(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        criminal = Criminal.objects.filter(Q(recorddate__gte=fd) & Q(recorddate__lte=td))
        criminalcount = Criminal.objects.filter(Q(recorddate__gte=fd) & Q(recorddate__lte=td)).count()
        d = {'criminal':criminal,'fd':fd,'td':td,'criminalcount':criminalcount,'newfir':newfir,'newfircount':newfircount}
        return render(request, 'betweendates_criminaldetails.html', d)
    d = {'newfir':newfir,'newfircount':newfircount}
    return render(request, 'betweendates_criminalreport.html',d)



def betweendates_criminaldetails(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    return render(request, 'betweendates_criminaldetails.html')

def completed_chargesheet(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    #policestationid = PoliceStation.objects.get(user=userid)
    fir = Fir.objects.filter(policestationid=policeid.policestationid,status="Charge Sheet Completed")
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'completed_chargesheet.html',d)


def betweendates_firreport(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        fir = Fir.objects.filter(Q(dateoffir__gte=fd) & Q(dateoffir__lte=td))
        fircount = Fir.objects.filter(Q(dateoffir__gte=fd) & Q(dateoffir__lte=td)).count()
        d = {'fir':fir,'fd':fd,'td':td,'fircount':fircount,'newfir':newfir,'newfircount':newfircount}
        return render(request, 'betweendates_firdetails.html', d)
    return render(request, 'betweendates_firreport.html')

def betweendates_firdetails(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    return render(request, 'betweendates_firdetails.html')

def search_criminal(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    terror = ""
    criminal=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            criminal = Criminal.objects.filter(criminalid=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'criminal':criminal,'terror':terror,'sd':sd,'newfir':newfir,'newfircount':newfircount}
    return render(request,'search_criminal.html',d)

def view_criminal(request,pid):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    criminal = Criminal.objects.get(id=pid)
    d = {'criminal':criminal,'newfir':newfir,'newfircount':newfircount}
    return render(request,'view_criminal.html', d)

def search_fir(request):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    terror = ""
    fir=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            fir = Fir.objects.filter(firno=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'fir':fir,'terror':terror,'sd':sd,'newfir':newfir,'newfircount':newfircount}
    return render(request,'search_fir.html',d)

def view_searchfir(request,pid):
    if not request.user.is_authenticated:
        return redirect('police_login')
    userid = User.objects.get(id=request.user.id)
    policeid = Police.objects.get(user=userid)
    newfir = Fir.objects.filter(policestationid=policeid.policestationid, status=None)
    newfircount = Fir.objects.filter(policestationid=policeid.policestationid, status=None).count()
    fir = Fir.objects.get(id=pid)
    d = {'fir':fir,'newfir':newfir,'newfircount':newfircount}
    return render(request,'view_searchfir.html', d)

def view_criminaladmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    criminal = Criminal.objects.all()
    d = {'criminal':criminal}
    return render(request,'view_criminaladmin.html', d)

def view_criminal_admin(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    criminal = Criminal.objects.get(id=pid)
    d = {'criminal':criminal}
    return render(request,'view_criminal_admin.html', d)

def view_firadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    fir = Fir.objects.all()
    d = {'fir':fir}
    return render(request,'view_firadmin.html', d)

def view_fir_admin(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    fir = Fir.objects.get(id=pid)
    d = {'fir':fir}
    return render(request,'view_fir_admin.html', d)


def betweendates_criminalreporta(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        criminal = Criminal.objects.filter(Q(recorddate__gte=fd) & Q(recorddate__lte=td))
        criminalcount = Criminal.objects.filter(Q(recorddate__gte=fd) & Q(recorddate__lte=td)).count()
        d = {'criminal':criminal,'fd':fd,'td':td,'criminalcount':criminalcount}
        return render(request, 'betweendates_criminaldetailsa.html', d)
    return render(request, 'betweendates_criminalreporta.html')

def betweendates_criminaldetailsa(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'betweendates_criminaldetailsa.html')



def betweendates_firreporta(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        fir = Fir.objects.filter(Q(dateoffir__gte=fd) & Q(dateoffir__lte=td))
        fircount = Fir.objects.filter(Q(dateoffir__gte=fd) & Q(dateoffir__lte=td)).count()
        d = {'fir':fir,'fd':fd,'td':td,'fircount':fircount}
        return render(request, 'betweendates_firdetailsa.html', d)
    return render(request, 'betweendates_firreporta.html')

def betweendates_firdetailsa(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'betweendates_firdetailsa.html')

def search_criminala(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    terror = ""
    criminal=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            criminal = Criminal.objects.filter(criminalid=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'criminal':criminal,'terror':terror,'sd':sd}
    return render(request,'search_criminala.html',d)


def search_fira(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    terror = ""
    fir=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            fir = Fir.objects.filter(firno=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'fir':fir,'terror':terror,'sd':sd}
    return render(request,'search_fira.html',d)

def chargesheetuser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    fir = Fir.objects.filter(userid=user,status="Charge Sheet Completed")
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    d = {'fir':fir,'firuser':firuser,'firusercount':firusercount}
    return render(request,'chargesheetuser.html',d)

def chargesheet_details(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    fir = Fir.objects.get(id=pid)
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    d = {'fir':fir,'firuser':firuser,'firusercount':firusercount}
    return render(request,'chargesheet_details.html',d)


def searchfiruser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    terror = ""
    fir=""
    sd=""
    userid = User.objects.get(id=request.user.id)
    firuser = Fir.objects.filter(status='Accepted', userid=userid)
    firusercount = Fir.objects.filter(status='Accepted', userid=userid).count()
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            user = User.objects.get(id=request.user.id)
            fir = Fir.objects.filter(firno=sd,userid=user)
            terror = "found"
        except:
            terror="notfound"
    d = {'fir':fir,'terror':terror,'sd':sd,'firuser':firuser,'firusercount':firusercount}
    return render(request,'searchfiruser.html',d)