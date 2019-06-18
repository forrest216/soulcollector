from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:soul_id>/', views.show, name='show'),
  path('<int:soul_id>/add_meal/', views.add_meal, name='add_meal'),
  path('<int:soul_id>/add_photo/', views.add_photo, name='add_photo'),
  path('<int:soul_id>/assoc_instrument/<int:instrument_id>/', views.assoc_instrument, name='assoc_instrument'),
  path('<int:soul_id>/unassoc_instrument/<int:instrument_id>/', views.unassoc_instrument, name='unassoc_instrument'),
  path('about/', views.about, name='about'),
  path('create/', views.SoulCreate.as_view(), name='souls_create'),
  path('<int:pk>/update/', views.SoulUpdate.as_view(), name='souls_update'),
  path('<int:pk>/delete/', views.SoulDelete.as_view(), name='souls_delete'),
  path('instruments/', views.InstrumentList.as_view(), name='instruments_index'),
  path('instruments/<int:pk>/', views.InstrumentDetail.as_view(), name='instruments_detail'),
  path('instruments/create/', views.InstrumentCreate.as_view(), name='instruments_create'),
  path('instruments/<int:pk>/update/', views.InstrumentUpdate.as_view(), name='instruments_update'),
  path('instruments/<int:pk>/delete/', views.InstrumentDelete.as_view(), name='instruments_delete'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
]
