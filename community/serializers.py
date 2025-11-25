from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated

from .models import Book, Comment, Category, BookCase, BookCaseItem


class BookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='title'
        )

    class Meta:
        model = Book
        fields = ['name', 'cover', 'description', 'category', 'score', 'author', 'publications', 'num_of_pages', 'date_writed']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'status', 'body', 'datetime_created']
        read_only_fields = ['user', 'status']
    
    def get_user(self, obj):
        return obj.user.username

    def create(self, validated_data):
        book_pk = self.context['book_pk']
        user = self.context['user']
        if not user.is_authenticated:
            raise NotAuthenticated('You must be logged in to post a comment.')
        return Comment.objects.create(user=user, book_id=book_pk, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    top_book = serializers.SlugRelatedField(
        queryset=Book.objects.all(),
        slug_field='name',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Category
        fields = ['title', 'description', 'top_book']
    
    def get_top_book(self, obj):
        return obj.top_book.name if obj.top_book else None


class BookCaseItemSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source='book', read_only=True)

    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
    )

    class Meta:
        model = BookCaseItem
        fields = ['id', 'book', 'book_detail', 'status', 'datetime_added']

    def validate(self, attrs):
        bookcase = self.context['bookcase']
        book = attrs.get('book')
        if BookCaseItem.objects.filter(bookcase=bookcase, book=book).exists():
            raise serializers.ValidationError("This book has already been added to your personal library.")
        return attrs


class BookCaseSerializer(serializers.ModelSerializer):
    items = BookCaseItemSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = BookCase
        fields = ['id', 'user', 'items']
        read_only_fields = ['user']
    
    def get_user(self, obj):
        return obj.user.username