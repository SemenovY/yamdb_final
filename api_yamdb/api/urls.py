"""API urls."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = "api"

router_v1 = SimpleRouter()

router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>[\d]+)/reviews",
    ReviewViewSet,
    basename="review",
)
router_v1.register(
    r"titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments",
    CommentViewSet,
    basename="comment",
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
