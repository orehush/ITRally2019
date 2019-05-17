from django_filters import rest_framework as filters

from api.models import Post


class PostFilterSet(filters.FilterSet):
    class Meta:
        model = Post
        fields = ('tags', 'author', 'reviewed_by', )
