from rest_framework.routers import SimpleRouter

from records.views import RecordViewSet

router = SimpleRouter()

router.register('', RecordViewSet, basename='records')

urlpatterns = router.urls
