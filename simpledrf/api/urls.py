from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter(trailing_slash='')
router.register('authors', views.AuthorViewSet)
router.register('reviewers', views.ReviewerViewSet)
router.register('tags', views.TagViewSet)
router.register('posts', views.PostViewSet)

urlpatterns = router.urls
