from django.urls import path
from cartapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.base_view),
    path('signup/', views.Signup_view,name='signup'),
    path('login/', views.Login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('contact/',views.Contact_view,name='contact'),
    path('products/',views.product_list,name='contact'),
     path('pluscart/',views.plus_cart,name='plus_cart'),
     path('minuscart/',views.minus_cart,name='minus_cart'),
     path('remove/<int:id>/',views.remove,name='remove'),
     path('carti/',views.log_view,name='log_view'),
     path('search/', views.product_search, name='product_search'),
     path('searchp/', views.search, name='search'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
      path('deleteadd/<int:id>/', views.delete_add, name='delete_add'),
      path('update_add/<int:id>/', views.Update_add, name='Update_add'),
      path('category/<str:category_name>', views.category_view, name='category_view'),
      path('product/<int:product_id>/',views.product_detailed_view,name='product_detailed_view'),

     
     
     


    path('cart/', views.view_cart),
    path('add/<int:product_id>/', views.add_to_cart,name='add_to_cart'),
] + static(settings.PRODUCTS_URL, document_root=settings.PRODUCTS_ROOT)