from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.create_listing, name='create_listing'),
    path('do_listing', views.do_listing, name='do_listing'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('listing/<int:listing_id>/bid', views.bid, name='bid'),
    path('listing/<int:listing_id>/saveWatchlist', views.saveWatchlist, name='saveWatchlist'),
    path('listing/<int:listing_id>/comment', views.comment, name='comment'),
    path('watchlist', views.view_watchlist, name='view_watchlist'),
    path('category', views.category, name="category"),
    path('category/<str:name_select>/', views.each_categories, name="categories"),
    path('listing/<int:listing_id>/close', views.close, name='close')    
]
