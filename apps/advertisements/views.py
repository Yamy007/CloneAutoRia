import datetime
from datetime import datetime

import requests
from better_profanity import profanity
from django.db.models import Avg
from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.advertisements.filter import StaticFilter
from apps.advertisements.models import (
    AdvertisementModel,
    CarModel,
    CounterCheck,
    DetailCarModel,
    StaticAdvertisementModel,
)
from apps.advertisements.serializers import (
    AdvertisementSerializers,
    AlbumSerializers,
    CarSerializer,
    DetailSerializers,
    StaticAdvertisementSerializers,
)
from apps.users.serializers import UserModelFunction
from core.exceptions.car_exception import ViewException
from core.permissions import IsAdmin, IsNotBlock, IsPremiumOrStaff, IsSellerAndNotBlock
from core.service.email_service import EmailService


class ListCreateCarView(ListCreateAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()


class RetrieveUpdateDestroyCarView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    http_method_names = (
        "put",
        "get",
        "delete",
    )


class CreateAdvertisement(GenericAPIView):
    permission_classes = (IsSellerAndNotBlock,)
    serializer_class = AdvertisementSerializers
    queryset = CarModel.objects.all()

    def post(self, *args, **kwargs):
        car = self.get_object()
        user = UserModelFunction.objects.get(pk=self.request.user.pk)
        data = self.request.data
        AdvertisementModel.objects.check_user_is_prem(user)
        serializers = AdvertisementSerializers(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.save(owner=user, car=car)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class RetrieveAdvertisement(RetrieveAPIView):
    permission_classes = (IsNotBlock,)
    serializer_class = AdvertisementSerializers

    def get_queryset(self):
        return AdvertisementModel.objects.filter(owner=self.request.user)


class ListAdvertisement(ListAPIView):
    permission_classes = (IsNotBlock,)
    serializer_class = AdvertisementSerializers
    queryset = AdvertisementModel.objects.exclude(is_active=False)


class UpdateDestroyAdvertisementView(UpdateAPIView, DestroyAPIView):
    permission_classes = (IsSellerAndNotBlock,)
    serializer_class = AdvertisementSerializers

    def get_queryset(self):
        return AdvertisementModel.objects.filter(owner_id=self.request.user.id)


class UpdateDescriptionAdvertisementView(UpdateAPIView):
    permission_classes = (IsSellerAndNotBlock,)
    serializer_class = DetailSerializers

    def get_object(self):
        pk = self.kwargs.get("pk")
        detail = get_object_or_404(DetailCarModel, pk=pk)
        advertisement = AdvertisementModel.objects.filter(
            description=detail,
            owner_id=self.request.user.id,
        ).first()
        if not advertisement:
            raise Http404
        return advertisement.description


class AddImageByAdvertisementView(GenericAPIView):
    permission_classes = (IsSellerAndNotBlock,)

    def get_queryset(self):
        return AdvertisementModel.objects.filter(owner_id=self.request.user.id)

    def post(self, *args, **kwargs):
        advertisement = self.get_object()
        data = self.request.data
        serializers = AlbumSerializers(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.save(advertisement=advertisement)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ViewAdvertisement(GenericAPIView):
    permission_classes = (IsNotBlock,)
    queryset = AdvertisementModel.objects.all()

    def post(self, *args, **kwargs):
        advertisement = self.get_object()
        user = UserModelFunction.objects.get(pk=self.request.user.pk)
        if StaticAdvertisementModel.objects.filter(
            user=user, advertisements=advertisement
        ).first():
            raise ViewException
        serializers = StaticAdvertisementSerializers(data={})
        serializers.is_valid(raise_exception=True)
        serializers.save(advertisements=advertisement, user=user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class ActivateAdvertisement(GenericAPIView):
    permission_classes = (IsSellerAndNotBlock,)

    def get_queryset(self):
        return AdvertisementModel.objects.filter(
            owner_id=self.request.user.id, is_active=False
        )

    def post(self, *args, **kwargs):
        advertisement = self.get_object()
        if CounterCheck.objects.filter(
            advertisement=advertisement, count__lt=3
        ).first():
            pass
        if profanity.contains_profanity(advertisement.info):
            counter = CounterCheck.objects.filter(advertisement=advertisement).first()

            if counter and counter.is_send:
                return Response(
                    {"detail": "Email send pls wait"}, status=status.HTTP_200_OK
                )

            if counter and counter.count < 3:
                setattr(counter, "count", counter.count + 1)
                counter.save()
            if counter and counter.count >= 3 and not counter.is_send:
                counter.is_send = True
                counter.save()
                EmailService.validate_email(user=self.request.user, id=advertisement.pk)
                return Response(
                    {"detail": "Email send pls wait"}, status=status.HTTP_200_OK
                )
            else:
                CounterCheck.objects.create(advertisement=advertisement, count=1)
            return Response(
                {"detail": f"fields info ${profanity.censor(advertisement.info)}"},
                status=status.HTTP_200_OK,
            )
        advertisement.is_active = True
        advertisement.save()
        return Response(
            AdvertisementSerializers(advertisement).data, status=status.HTTP_200_OK
        )


class SendToCourseView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        response = requests.get(
            f"https://api.privatbank.ua/p24api/exchange_rates?date={datetime.now().strftime('%d.%m.%Y')}"
        )
        return Response(response.json(), status=status.HTTP_200_OK)


class InfoAboutViewAdvertisement(ListAPIView):
    permission_classes = (IsPremiumOrStaff,)
    serializer_class = StaticAdvertisementSerializers
    filterset_class = StaticFilter

    def get_queryset(self, *args, **kwargs):
        return StaticAdvertisementModel.objects.filter(
            advertisements_id=self.kwargs.get("pk")
        )

    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response({"count_view": queryset.count()}, status=status.HTTP_200_OK)


class AVGCarView(GenericAPIView):
    permission_classes = (IsPremiumOrStaff,)
    serializer_class = AdvertisementSerializers
    queryset = AdvertisementModel.objects.exclude(is_active=False)

    def get(self, *args, **kwargs):
        advertisement = self.get_object()
        car, region = (
            advertisement.car,
            advertisement.region,
        )
        if self.request.GET.get("all"):
            advertisement = AdvertisementModel.objects.filter(car=car)
        else:
            advertisement = AdvertisementModel.objects.filter(car=car, region=region)
        type_price = self.request.GET.get("type_price")
        if type_price:
            advertisement = advertisement.filter(type_price=type_price)
        else:
            advertisement = advertisement.filter(type_price="UAH")
        average_price = advertisement.aggregate(avg_price=Avg("price"))["avg_price"]
        return Response({"average_price": average_price}, status=status.HTTP_200_OK)
