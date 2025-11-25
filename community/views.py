from django.db.models import Prefetch
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .filters import BookFilter
from .models import Book, BookCaseItem, Comment, Category, BookCase
from .paginations import DefaultPaginations
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminForEdit
from .serializers import BookCaseSerializer, BookSerializer, CategorySerializer, CommentSerializer, BookCaseItemSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ["get", "post", "delete"]
    pagination_class = DefaultPaginations
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'category__title']
    ordering_fields = ['name', 'score']
    filterset_class = BookFilter

    def get_queryset(self):
        return Book.objects.select_related('category').all()

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [AllowAny()]
        

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminForEdit]
    http_method_names = ['get', 'post', 'delete', 'patch']
    filter_backends = [OrderingFilter]
    ordering_fields = ['datetime_created']
    pagination_class = DefaultPaginations
        

    def get_queryset(self):
        book_pk = self.kwargs['book_pk']
        return Comment.objects.filter(book_id=book_pk).select_related('user').all()
    
    def get_serializer_context(self):
        return {'book_pk': self.kwargs['book_pk'], 'user': self.request.user}


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Category.objects.select_related('top_book').all()


class BookCaseViewSet(ReadOnlyModelViewSet):
    serializer_class = BookCaseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    def get_queryset(self):
        user = self.request.user
        queryset = BookCase.objects.prefetch_related(Prefetch(
                'items',
                BookCaseItem.objects.select_related('book__category')
            )).select_related('user')
        
        if user.is_staff:
            return queryset.all()
        return queryset.filter(user=user)


class UserBookCaseItemViewSet(ModelViewSet):
    serializer_class = BookCaseItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @cached_property
    def bookcase(self):
        return get_object_or_404(BookCase, user=self.request.user)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = BookCaseItem.objects.select_related('bookcase', 'book', 'book__category')

        if pk is not None:
            return queryset.filter(bookcase=self.bookcase, pk=pk)
        return queryset.filter(bookcase=self.bookcase)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['bookcase'] = self.bookcase
        return context

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if BookCaseItem.objects.filter(bookcase=self.bookcase, book=book).exists():
            raise ValidationError("This book has already been added to your personal library.")
        serializer.save(bookcase=self.bookcase)


class BookCaseItemViewSet(ModelViewSet):
    serializer_class = BookCaseItemSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @cached_property
    def bookcase(self):
        pk = self.kwargs['bookcase_pk']
        return get_object_or_404(BookCase, pk=pk)

    def get_queryset(self):
        return BookCaseItem.objects.select_related('bookcase', 'book', 'book__category').filter(bookcase=self.bookcase)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if BookCaseItem.objects.filter(bookcase=self.bookcase, book=book).exists():
            raise ValidationError("This book has already been added to your personal library.")
        serializer.save(bookcase=self.bookcase)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['bookcase'] = self.bookcase
        return context