from rest_framework.routers import DefaultRouter

from apps.accounts.viewsets import UserViewSet
from apps.groups.viewsets import GroupViewSet
from apps.finances.viewsets import ExpenseViewSet


router = DefaultRouter()

router.register("users", UserViewSet)

router.register("groups", GroupViewSet)
router.register("expenses", ExpenseViewSet)

