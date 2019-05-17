from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.filters import PostFilterSet
from api.permissions import IsAuthorOrReadOnly, IsReviewer
from api.serializers import *


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List/retrieve tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List/retrieve authors
    """
    queryset = Author.objects.filter(is_active=True)
    serializer_class = AuthorSerializer
    permission_classes = (AllowAny, )


class ReviewerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List/retrieve experienced reviewers
    """
    queryset = Reviewer.objects.filter(is_active=True, level__gte=1)
    serializer_class = ReviewerSerializer
    permission_classes = (AllowAny, )


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """
    queryset = Post.objects.exclude(is_deleted=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    filterset_class = PostFilterSet

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['put'],
            permission_classes=[IsReviewer],
            serializer_class=serializers.Serializer)
    def approve(self, request, **kwargs):
        """
        Endpoint to approve post by reviewer
        """
        post = self.get_object()
        post.reviewed_by.add(request.user.reviewer)
        serializer = PostSerializer(post)
        return Response(serializer.data)
