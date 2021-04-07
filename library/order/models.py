from django.db import models, DataError, IntegrityError

from authentication.models import CustomUser
from author.models import Author
from book.models import Book
import datetime


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now=True)
    #end_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=15))
    end_at = models.DateTimeField(null=True)
    plated_end_at = models.DateTimeField(default=None)

    def __str__(self):
        if self.end_at is None:
            return ("'id': " + str(self.id) + ", 'user': CustomUser(id=" + str(self.user.id) + "), 'book': Book(id=" +
                    str(self.book.id) + "), 'created_at': '" +
                    str(self.created_at) + "', 'end_at': None, 'plated_end_at': '" +
                    str(self.plated_end_at) + "'")
        else:
            return ("'id': " + str(self.id) + ", 'user': CustomUser(id=" + str(self.user.id) + "), 'book': Book(id=" +
                    str(self.book.id) + "), 'created_at': '" +
                    str(self.created_at) + "', 'end_at': '" + str(self.end_at) + "', 'plated_end_at': '" +
                    str(self.plated_end_at) + "'")

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {'id': self.id,
                'user': self.user,
                'book': self.book,
                'created_at': int(self.created_at.timestamp()),
                'end_at': int(self.end_at.timestamp()),
                'plated_end_at': int(self.plated_end_at.timestamp())}

    @staticmethod
    def create(user, book, plated_end_at):
        try:
            if (user is None) or (book is None) or (plated_end_at is None):
                raise DataError
            if len(Order.objects.filter(end_at=None).filter(book=book))>= book.count:
                return None
            if user not in CustomUser.objects.filter(id=user.id):
                raise ValueError

            new_order = Order.objects.create(user=user,
                                             book=book,
                                             plated_end_at=plated_end_at)

            return new_order
        except IntegrityError:
            return None
        except DataError:
            return None
        except ValueError:
            return None

    @staticmethod
    def get_by_id(order_id):
        if Order.objects.filter(id=order_id):
            return Order.objects.get(id=order_id)
        else:
            return None
        pass

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            Order.objects.filter(id=self.id).update(plated_end_at=plated_end_at)
        if end_at is not None:
            Order.objects.filter(id=self.id).update(end_at=end_at)

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at=None))

    @staticmethod
    def delete_by_id(order_id):
        if Order.objects.filter(id=order_id):
            Order.objects.filter(id=order_id).delete()
            return True
        else:
            return False