from django.urls import path
from . import views
# routes going to be here
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #spider url
    path('spiders/', views.spiders_index, name='index'),
    path('spiders/<int:spider_id>/', views.spiders_detail, name='detail'),
    path('spiders/create/', views.SpiderCreate.as_view(), name='spiders_create'),
    path('spiders/<int:pk>/update/', views.SpiderUpdate.as_view(), name='spiders_update'),
    path('spiders/<int:pk>/delete/', views.SpiderDelete.as_view(), name='spiders_delete'),
    path('spiders/<int:spider_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    #add photo path
    path('spiders/<int:spider_id>/add_photo/', views.add_photo, name='add_photo'),
    #associate decor with spider
    path('spiders/<int:spider_id>/assoc_decor/<int:decoration_id>/', views.assoc_decor, name='assoc_decor'),
    #unassociate decor (delete)
    path('spiders/<int:spider_id>/unassoc_decor/<int:decoration_id>/', views.unassoc_decor, name='unassoc_decor'),
    #decor url
    path('decorations/', views.DecorationList.as_view(),name='decorations_index'),
    path('decorations/<int:pk>/', views.DecorationDetail.as_view(), name='decorations_detail'),
    path('decorations/create/', views.DecorationCreate.as_view(), name='decorations_create'),
    path('decorations/<int:pk>/update/', views.DecorationUpdate.as_view(), name='decorations_update'),
    path('decorations/<int:pk>/delete/', views.DecorationDelete.as_view(), name='decorations_delete'),
    #authentication
    path('accounts/signup/', views.signup, name='signup'),
]


