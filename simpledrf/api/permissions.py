from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from api.models import Post


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.method == 'post':
            return hasattr(request.user, 'author')
        return super(IsAuthorOrReadOnly, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj: Post):
        return (
            super(IsAuthorOrReadOnly, self).has_object_permission(request, view, obj) and
            hasattr(request.user, 'author') and
            obj.author == request.user.author
        )


class IsReviewer(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super(IsReviewer, self).has_permission(request, view) and
            hasattr(request.user, 'reviewer')
        )
