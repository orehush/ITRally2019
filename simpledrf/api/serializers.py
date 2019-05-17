from django.contrib.auth.models import User
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers

from api.models import Tag, Author, Reviewer, Post


class CurrentChildUserDefault(serializers.CurrentUserDefault):
    def __call__(self):
        return self.user.child


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', )


class AuthorSerializer(UserSerializer):
    class Meta:
        model = Author
        fields = UserSerializer.Meta.fields + ('rating', )


class ReviewerSerializer(UserSerializer):
    class Meta:
        model = Reviewer
        fields = UserSerializer.Meta.fields + ('level', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ('reviewed_by', 'modified', 'created', )
        exclude = ('is_deleted', )

    author = PresentablePrimaryKeyRelatedField(
        presentation_serializer=AuthorSerializer,
        queryset=Author.objects.all(),
        default=serializers.CreateOnlyDefault(CurrentChildUserDefault())
    )
    tags = PresentablePrimaryKeyRelatedField(
        presentation_serializer=TagSerializer, many=True,
        queryset=Tag.objects.all()
    )
    reviewed_by = ReviewerSerializer(many=True, read_only=True)
