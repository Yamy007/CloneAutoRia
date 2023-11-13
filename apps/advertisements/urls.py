from django.urls import path

from apps.advertisements.views import (
    ActivateAdvertisement,
    AddImageByAdvertisementView,
    AVGCarView,
    CreateAdvertisement,
    InfoAboutViewAdvertisement,
    ListAdvertisement,
    ListCreateCarView,
    RetrieveAdvertisement,
    RetrieveUpdateDestroyCarView,
    SendToCourseView,
    UpdateDescriptionAdvertisementView,
    UpdateDestroyAdvertisementView,
    ViewAdvertisement,
)

urlpatterns = [
    path("notice/car", ListCreateCarView.as_view(), name="notice_car_create"),
    path(
        "notice/car/<int:pk>",
        RetrieveUpdateDestroyCarView.as_view(),
        name="notice_car_retrieve",
    ),
    path("notice/create/<int:pk>", CreateAdvertisement.as_view(), name="notice"),
    path("notice/<int:pk>", RetrieveAdvertisement.as_view(), name="notice"),
    path("notice/list", ListAdvertisement.as_view(), name="notice_list"),
    path(
        "notice/settings/<int:pk>",
        UpdateDestroyAdvertisementView.as_view(),
        name="notice_list",
    ),
    path(
        "notice/detail/<int:pk>",
        UpdateDescriptionAdvertisementView.as_view(),
        name="notice_description",
    ),
    path(
        "notice/image/<int:pk>",
        AddImageByAdvertisementView.as_view(),
        name="notice_description",
    ),
    path(
        "notice/view/<int:pk>",
        ViewAdvertisement.as_view(),
        name="notice_description",
    ),
    path(
        "notice/course",
        SendToCourseView.as_view(),
        name="notice_description",
    ),
    path(
        "notice/activate/<int:pk>",
        ActivateAdvertisement.as_view(),
        name="notice_description",
    ),
    path(
        "notice/static/view/<int:pk>",
        InfoAboutViewAdvertisement.as_view(),
        name="notice_description",
    ),
    path(
        "notice/static/avg/<int:pk>",
        AVGCarView.as_view(),
        name="notice_description",
    ),
    # path("notice/view/<int:pk>", ViewAdvertisement.as_view(), name="notice"),
]
