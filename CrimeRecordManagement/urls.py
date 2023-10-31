"""CrimeRecordManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crimerecord.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home, name='admin_home'),
    path('add_policestation',add_policestation, name='add_policestation'),
	path('add_policestation/',add_policestation, name='add_policestation'),
    path('manage_policestation',manage_policestation, name='manage_policestation'),
    path('edit_policestation/<int:pid>',edit_policestation, name='edit_policestation'),
    path('delete_policestation/<int:pid>',delete_policestation, name='delete_policestation'),
    path('add_police', add_police, name='add_police'),
    path('manage_police', manage_police, name='manage_police'),
    path('edit_police/<int:pid>',edit_police, name='edit_police'),
    path('delete_police/<int:pid>',delete_police, name='delete_police'),
    path('add_category',add_category, name='add_category'),
    path('manage_category',manage_category, name='manage_category'),
    path('edit_category/<int:pid>',edit_category, name='edit_category'),
    path('delete_category/<int:pid>',delete_category, name='delete_category'),
    path('logout',Logout, name='logout'),
    path('change_passwordadmin',change_passwordadmin, name='change_passwordadmin'),
    path('police_login',police_login,name='police_login'),
    path('police_home',police_home, name='police_home'),
    path('add_criminal',add_criminal, name='add_criminal'),
    path('manage_criminal',manage_criminal, name='manage_criminal'),
    path('edit_criminal/<int:pid>',edit_criminal, name='edit_criminal'),
    path('change_image/<int:pid>',change_image, name='change_image'),
    path('delete_criminal/<int:pid>',delete_criminal, name='delete_criminal'),
    path('change_passwordpolice',change_passwordpolice, name='change_passwordpolice'),
    path('user_signup',user_signup, name='user_signup'),
    path('user_login',user_login,name='user_login'),
    path('user_home',user_home, name='user_home'),
    path('change_passworduser',change_passworduser, name='change_passworduser'),
    path('user_profile',user_profile, name='user_profile'),
    path('fir_form',fir_form, name='fir_form'),
    path('police_profile',police_profile, name='police_profile'),
    path('new_fir',new_fir, name='new_fir'),
    path('fir_history',fir_history, name='fir_history'),
    path('view_firdetails/<int:pid>',view_firdetails, name='view_firdetails'),
    path('fir_details/<int:pid>',fir_details, name='fir_details'),
    path('approved_fir',approved_fir, name='approved_fir'),
    path('cancelled_fir',cancelled_fir, name='cancelled_fir'),
    path('all_fir',all_fir,name='all_fir'),
    path('new_chargesheet',new_chargesheet,name='new_chargesheet'),
    path('completed_chargesheet',completed_chargesheet,name='completed_chargesheet'),
    path('fill_chargesheetdetails/<int:pid>',fill_chargesheetdetails,name='fill_chargesheetdetails'),
    path('betweendates_criminalreport',betweendates_criminalreport,name='betweendates_criminalreport'),
    path('betweendates_criminaldetails',betweendates_criminaldetails,name='betweendates_criminaldetails'),
    path('betweendates_firreport',betweendates_firreport,name='betweendates_firreport'),
    path('betweendates_firdetails',betweendates_firdetails,name='betweendates_firdetails'),
    path('search_criminal',search_criminal,name='search_criminal'),
    path('view_criminal/<int:pid>',view_criminal,name='view_criminal'),
    path('search_fir',search_fir,name='search_fir'),
    path('view_searchfir/<int:pid>',view_searchfir,name='view_searchfir'),
    path('view_criminaladmin',view_criminaladmin,name='view_criminaladmin'),
    path('view_criminal_admin/<int:pid>',view_criminal_admin,name='view_criminal_admin'),
    path('view_firadmin',view_firadmin,name='view_firadmin'),
    path('view_fir_admin/<int:pid>',view_fir_admin,name='view_fir_admin'),
    path('betweendates_criminalreporta',betweendates_criminalreporta,name='betweendates_criminalreporta'),
    path('betweendates_criminaldetailsa',betweendates_criminaldetailsa,name='betweendates_criminaldetailsa'),
    path('betweendates_firreporta',betweendates_firreporta,name='betweendates_firreporta'),
    path('betweendates_firdetailsa',betweendates_firdetailsa,name='betweendates_firdetailsa'),
    path('search_criminala',search_criminala,name='search_criminala'),
    path('search_fira',search_fira,name='search_fira'),
    path('chargesheetuser',chargesheetuser,name='chargesheetuser'),
    path('chargesheet_details/<int:pid>',chargesheet_details,name='chargesheet_details'),
    path('searchfiruser',searchfiruser,name='searchfiruser'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
