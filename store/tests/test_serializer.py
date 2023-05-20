from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username='test_username', first_name='Alex', last_name='Smith')
        self.user2 = User.objects.create(username='test_username2')
        self.user3 = User.objects.create(username='test_username3')
        book_1 = Book.objects.create(name='TestBook 1', price=25,
                                     author_name='Author 1', owner=self.user)
        book_2 = Book.objects.create(name='TestBook 2', price=55,
                                     author_name='Author 2', owner=self.user)

        UserBookRelation.objects.create(user=self.user, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user2, book=book_1, like=True,
                                        rate=5)
        user_book_3 = UserBookRelation.objects.create(user=self.user3, book=book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=self.user, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=self.user2, book=book_2, like=False,
                                        rate=4)
        UserBookRelation.objects.create(user=self.user3, book=book_2, like=True)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'TestBook 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'owner': self.user.id,
                'readers': [
                    {
                        'first_name': 'Alex',
                        'last_name': 'Smith'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                ],
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'test_username'
            },
            {
                'id': book_2.id,
                'name': 'TestBook 2',
                'price': '55.00',
                'author_name': 'Author 2',
                'owner': self.user.id,
                'readers': [
                    {
                        'first_name': 'Alex',
                        'last_name': 'Smith'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                ],
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': 'test_username'
            }
        ]

        self.assertEqual(expected_data, data)
