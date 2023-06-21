from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.home, name="home"),
    path(
        "about/", views.about, name="about"),
    path(
        "destinations/", views.destinations_index, name="index"),
    path(
        "destinations/<int:destination_id>/", views.destinations_detail, name="detail"
    ),
    path(
        "destinations/create/",
        views.DestinationCreate.as_view(),
        name="destinations_create",
    ),
    path(
        "destinations/<int:pk>/update/",
        views.DestinationUpdate.as_view(),
        name="destinations_update",
    ),
    path(
        "destinations/<int:pk>/delete/",
        views.DestinationDelete.as_view(),
        name="destinations_delete",
    ),
    path(
        "destinations/<int:destination_id>/add_itinerary/",
        views.add_itinerary,
        name="add_itinerary",
    ),
    path(
        'destinations/<int:destination_id>/add_media/',
        views.add_media,
        name='add_media'
    ),
    path(
      'accounts/signup/',
      views.signup,
      name='signup'),

    path(
      'destinations/weather/',
      views.weather,
      name='weather',
    ),

    path(
      'blogs/blog_form/',
      views.BlogPostCreate.as_view(),
      name='blog_create',
    ),
    path(
        '', views.home, name='blogs_index'
    )
]
