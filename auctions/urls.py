from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
<<<<<<< HEAD
    path('create_listing', views.create_listing, name='create_listing'),
    path('do_listing', views.do_listing, name='do_listing')
=======
    path('create_listing/<int:listing_id>', views.create_listing, name='create_listing')
>>>>>>> 9d7072ac210c4f935d70277331a3c0cd4ad1283b
]
