from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)
    serial = models.CharField(max_length=10, blank=True, null=True, unique=True)
    categories = models.ManyToManyField(Category, blank=True)
    cover = models.TextField(max_length=100000, blank=True, null=True)
    author = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=25000, blank=True, null=True)
    available = models.IntegerField(default=0)
    price = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.firstname

    @property
    def full_name(self):
        return "{} {}".format(self.firstname, self.lastname)


class Borrow(models.Model):
    book = models.ManyToManyField(Book)
    student = models.ManyToManyField(Student)
    qty = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=25)
    approved = models.BooleanField(default=False)


@receiver(pre_save, sender=Book)
def set_serial(sender, instance, *args, **kwargs):
    if not instance.id:
        last_obj = Book.objects.last()
        if last_obj:
            if last_obj.serial:
                serial = str(int(last_obj.serial) + 1).zfill(6)
                instance.serial = serial
            else:
                raise FieldError("Book object <{}>  serial does not exist".format(last_obj.id))
        else:
            instance.serial = '1'.zfill(6)
    # else:
    #     # can't update without serial if you don't want
    #     # comment out this else block
    #     if not instance.serial:
    #         raise FieldError("Book object {} does not have serial".format(instance.id))
