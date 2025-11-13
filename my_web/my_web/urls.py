"""
URL configuration for my_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# noinspection PyUnresolvedReferences
from  my_web import views
# noinspection PyUnresolvedReferences
from my_web.views import update_cart,remove_cart_item,checkout,add_to_cart

# noinspection PyUnresolvedReferences
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePage ,name='homePage'),
    path('jewellery', views.jewellery),
    path('electronic', views.electronic),
    path('fashion', views.fashion ),
    path('about/', views.about ),
    path('contact/', views.contact, name='contact'),
    path('registration',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("buy_now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path('update-cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove-cart-item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path("order/", views.order_summary, name="order_summary"),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
