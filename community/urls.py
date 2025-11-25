from rest_framework_nested import routers

from django.urls import path

from . import views


router = routers.DefaultRouter()
router.register('books', views.BookViewSet, basename='book')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('bookcase', views.BookCaseViewSet, basename='bookcase')


books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('comments', views.CommentViewSet, basename='book-comment')

bookcase_router = routers.NestedDefaultRouter(router, 'bookcase', lookup='bookcase')
bookcase_router.register('items', views.BookCaseItemViewSet, basename='bookcase-items')

urlpatterns = [
    path('bookcase/items/', views.UserBookCaseItemViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('bookcase/items/<int:pk>/', views.UserBookCaseItemViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
] + router.urls + books_router.urls + bookcase_router.urls