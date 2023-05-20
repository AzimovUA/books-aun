from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', first_name='Alex', last_name='Smith')
        self.user2 = User.objects.create(username='test_username2')
        self.user3 = User.objects.create(username='test_username3')
        self.book_1 = Book.objects.create(name='TestBook 1', price=25,
                                          author_name='Author 1', owner=self.user)

        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True,
                                        rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
