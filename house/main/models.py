import uuid
import os
import hashlib
import datetime
import unicodedata

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import utc

from sorl.thumbnail import ImageField


def now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def identifier_maker(length):
    def maker():
        return uuid.uuid4().hex[:length]
    return maker


class Address(models.Model):
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, default='United States')
    timezone = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    added = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)


class House(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    owners = models.ManyToManyField(User, related_name='houses')
    address = models.ForeignKey(Address, null=True)

    added = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)

    def __repr__(self):
        return "<%s: %r>" % (self.__class__.__name__, self.address.line1)

    @classmethod
    def get_house(self, user):
        return self.objects.get(owners=user)


def _upload_path(tag):
    def _upload_path_tagged(instance, filename):
        if isinstance(filename, unicode):
            filename = (
                unicodedata
                .normalize('NFD', filename)
                .encode('ascii', 'ignore')
            )
        _now = now()
        path = os.path.join(
#            "%05d" % instance.pk,
            _now.strftime('%Y'),
            _now.strftime('%m'),
            _now.strftime('%d')
        )
        hashed_filename = (hashlib.md5(filename +
                           str(now().microsecond)).hexdigest())
        __, extension = os.path.splitext(filename)
        return os.path.join(tag, path, hashed_filename + extension)
    return _upload_path_tagged


class Photo(models.Model):
    house = models.ForeignKey(House)
    photo = ImageField(upload_to=_upload_path('photos'))
    cover = models.DateTimeField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    added_by = models.ForeignKey(User)
    added = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)

    def set_cover_photo(self):
        self.cover = now()

    @classmethod
    def get_cover_photo(self, house):
        _qs = self.objects.filter(house=house).exclude(cover=None)
        for p in _qs.order_by('-cover')[:1]:
            return p


class Document(models.Model):
    house = models.ForeignKey(House)
    picture = ImageField(upload_to=_upload_path('documents'), blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    searchable_text = models.TextField(blank=True, null=True)
    text_extracted = models.BooleanField(default=False)
    added_by = models.ForeignKey(User)

    added = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)


class Invitation(models.Model):
    house = models.ForeignKey(House)
    user = models.ForeignKey(User)
    email_address = models.EmailField()
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    identifier = models.CharField(max_length=32, default=identifier_maker(16))

    added = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)


@receiver(models.signals.pre_save, sender=House)
@receiver(models.signals.pre_save, sender=Photo)
@receiver(models.signals.pre_save, sender=Document)
@receiver(models.signals.pre_save, sender=Address)
@receiver(models.signals.pre_save, sender=Invitation)
def update_modified(sender, instance, raw, *args, **kwargs):
    if raw:
        return
    instance.modified = now()
