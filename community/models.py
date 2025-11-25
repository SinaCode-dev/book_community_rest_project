from django.conf import settings
from django.db import models


class Book(models.Model):
    BOOK_SCORE_VERYBAD = 1
    BOOK_SCORE_BAD = 2
    BOOK_SCORE_NORMAL = 3
    BOOK_SCORE_GOOD = 4
    BOOK_SCORE_PERFECT = 5
    BOOK_SCORE = [
        (BOOK_SCORE_VERYBAD, 'Very bad'),
        (BOOK_SCORE_BAD, 'Bad'),
        (BOOK_SCORE_NORMAL, 'Normal'),
        (BOOK_SCORE_GOOD, 'Good'),
        (BOOK_SCORE_PERFECT, 'Perfect'),
    ]

    name = models.CharField(max_length=250)
    cover = models.ImageField(verbose_name="Book Cover", upload_to="book/book_cover/", blank=True)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='books')
    score = models.PositiveIntegerField(choices=BOOK_SCORE)
    author = models.CharField(max_length=250)
    publications = models.CharField(max_length=250)
    num_of_pages = models.PositiveIntegerField()
    date_writed = models.DateField()

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOTAPPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, "Waiting"),
        (COMMENT_STATUS_APPROVED, "Approved"),
        (COMMENT_STATUS_NOTAPPROVED, "Not Approved"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING, max_length=2)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    top_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return f'{self.title}'


class BookCase(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s bookcase"


class BookCaseItem(models.Model):
    READING_STATUS_UNREAD = "ur"
    READING_STATUS_READ = "r"
    READING_STATUS_IS_READING = "ir"
    READING_STATUS_WANT_TO_READ = "wr"
    READING_STATUS = [
        (READING_STATUS_UNREAD, 'Unread'),
        (READING_STATUS_READ, 'Read'),
        (READING_STATUS_IS_READING, 'Is reading'),
        (READING_STATUS_WANT_TO_READ, 'Want to read'),
    ]

    bookcase = models.ForeignKey(BookCase, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(choices=READING_STATUS, default=READING_STATUS_WANT_TO_READ, max_length=2)
    datetime_added = models.DateTimeField(auto_now_add=True)