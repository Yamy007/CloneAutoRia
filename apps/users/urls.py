from django.urls import path

from apps.users.views import (
    AllUsers,
    BlockedUser,
    CreateAdminUser,
    CreateUser,
    CreateUserAsSeller,
    DeletePremiumAccount,
    GetMeUser,
    GetPremiumAccount,
    GetTimePremium,
    GetUserById,
    SetDestroyTimePremium,
    UnBlockedUser,
    UpdateProfileUser,
    UpdateProfileUserById,
    UpdateUserPermissions,
)

urlpatterns = [
    # create
    path("register", CreateUser.as_view(), name="register"),
    path("register/seller", CreateUserAsSeller.as_view(), name="register_seller"),
    path("register/admin", CreateAdminUser.as_view(), name="register_seller"),
    # settings
    path("update/<int:pk>", UpdateUserPermissions.as_view(), name="update_user"),
    path("update/profile", UpdateProfileUser.as_view(), name="update_profile"),
    path(
        "update/profile/<int:pk>",
        UpdateProfileUserById.as_view(),
        name="update_profile_by_id",
    ),
    # show
    path("show/users", AllUsers.as_view(), name="show_all_users"),
    path("show/user/<int:pk>", GetUserById.as_view(), name="show_user_by_id"),
    path("show/user/me", GetMeUser.as_view(), name="show_user_me"),
    # block
    path("block/block/<int:pk>", BlockedUser.as_view(), name="block_block"),
    path("block/unblock/<int:pk>", UnBlockedUser.as_view(), name="block_unblock"),
    # premium
    path(
        "premium/add_premium/<int:pk>", GetPremiumAccount.as_view(), name="premium_add"
    ),
    path(
        "premium/del_premium/<int:pk>",
        DeletePremiumAccount.as_view(),
        name="premium_del",
    ),
    # time_premium
    path("premium/get_time/premium", GetTimePremium.as_view(), name="premium_get_time"),
    path(
        "premium/set_time/premium/<int:pk>",
        SetDestroyTimePremium.as_view(),
        name="premium_set_time",
    ),
]
