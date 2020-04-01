from rest_framework.routers import DefaultRouter

from subscribe.api.v1.views import SubscribeView

router = DefaultRouter()
router.register("subscribe", SubscribeView, basename="subscribe")

urlpatterns = router.urls
