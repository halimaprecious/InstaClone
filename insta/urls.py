from django.urls import re_path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views



urlpatterns =[
    re_path(r'^$',views.home ,name='home'),
    re_path(r'^tinymce/', include('tinymce.urls')),

    re_path(r'^accounts/profile/', views.add_profile, name='add_profile'),
    re_path(r"^profile/(\d+)", views.profile, name="profile"),
    

    re_path(r'^login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name = 'login'),

    re_path(r'^search/', views.search_results, name='search_results'),
    re_path(r'^image/(\d+)',views.get_image_by_id,name ='image'),
    re_path(r'^upload/', views.update_image, name='upload'),


    re_path(r'^comment/(?P<pk>\d+)',views.add_comment,name='comment'),
    re_path(r'^like/(?P<operation>.+)/(?P<pk>\d+)',views.like, name='like'),
    re_path(r'^all/(?P<pk>\d+)', views.all, name='all'),
    re_path(r'^follow/(?P<operation>.+)/(?P<id>\d+)',views.follow,name='follow'),



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
