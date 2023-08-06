# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from decimal import Decimal
from typing import List
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Field
from django.utils import timezone
import django
if django.VERSION >= (4, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _

from gpp.datetimes import dt
from gpp.model.fields import CompressedTextField


def default_value(field: Field):
    """
        models.field에 형태에 임의의 값 반환

    :param field: models.Field instance
    :type field: models.Field
    :return:
    :rtype: Union[int, date, time, datetime, timedelta, byte, int, ...]
    """
    mapping = [
        (models.CharField, '1'),
        (models.IntegerField, 1),
        (models.DateTimeField, dt(2020, 1, 1)),
        (models.DateField, dt(2020, 1, 1).date()),
        (models.TimeField, dt(2020, 1, 1).time()),
        (models.DecimalField, Decimal('123.456')),
        (models.DurationField, timedelta(seconds=1)),
        (models.BooleanField, True),
        (models.UUIDField, UUID('280a8a4d-a27f-4d01-b031-2a003cc4c039')),
        (CompressedTextField, 'abc'),
        (models.BinaryField, b'abc'),
        (models.TextField, '1'),
        (models.GenericIPAddressField, '1.1.1.1'),
        (models.FilePathField, '/a.txt'),
        (models.FloatField, 1.0),
    ]
    for f, v in mapping:
        if isinstance(field, f):
            return v


class BaseModelMixin(models.Model):
    """
        PK mixin
    """
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(_('created date'), blank=True, editable=False)
    modified = models.DateTimeField(_('modified date'), blank=True, editable=False)

    class Meta:
        abstract = True

    @classmethod
    def dummy(cls, save=False, **kwargs):
        """
            dummy 데이터 생성

        :param save: DB 저장 여부
        :type save: bool
        :param kwargs: parameter
        :type kwargs: dict
        :return: instance
        :type: Type[cls]
        """
        for field in cls._meta.fields:
            if field.attname in {'id'}:
                continue
            if field.attname not in kwargs:
                kwargs.update({field.attname: default_value(field)})

        instance = cls(**kwargs)
        if save:
            instance.save()
        return instance

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created:
            self.created = now
            if 'update_fields' in kwargs:
                kwargs['update_fields'].append('created')

        update_fields = kwargs.get('update_fields', None)
        if not update_fields:
            self.modified = now
        elif isinstance(update_fields, list) and 'modified' not in update_fields:
            self.modified = now
            update_fields.append('modified')

        super(BaseModelMixin, self).save(*args, **kwargs)


class ArchiveModelMixin(models.Model):
    """
        model 삭제시 archive
    """

    archive_date = models.DateTimeField(_('created date'), blank=True, editable=False)

    old_pk = models.BigIntegerField(_('old pk'), db_index=True, blank=False, editable=False)

    archive_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='+',
        null=True, blank=False, db_constraint=False,
        db_index=False,
    )

    class Meta:
        abstract = True


class TaskModelMixin(models.Model):
    """
        Async Task 모델 Mixin
        Task Status와 관련된 field 모음.
    """
    CHOICE_TASK_STATUS_QUEUED = 10  # push to MQ
    CHOICE_TASK_STATUS_PROGRESSING = 20  # pop from MQ
    CHOICE_TASK_STATUS_ERROR = 30  # something wrong...
    CHOICE_TASK_STATUS_COMPLETED = 40  # complete

    CHOICE_TASK_STATUS = (
        (CHOICE_TASK_STATUS_QUEUED, _('in queued')),
        (CHOICE_TASK_STATUS_PROGRESSING, _('in processing')),
        (CHOICE_TASK_STATUS_ERROR, _('error')),
        (CHOICE_TASK_STATUS_COMPLETED, _('completed')),
    )

    task_status = models.PositiveSmallIntegerField(
        _('status of crawling task'),
        choices=CHOICE_TASK_STATUS,
        default=CHOICE_TASK_STATUS_QUEUED,
    )
    queued_datetime = models.DateTimeField(_('queued datetime'), null=True, blank=True, default=None)
    processing_datetime = models.DateTimeField(_('processing datetime'), null=True, blank=True, default=None)
    error_datetime = models.DateTimeField(_('error datetime'), null=True, blank=True, default=None)
    completed_datetime = models.DateTimeField(_('completed datetime'), null=True, blank=True, default=None)

    def set_completed(self, save: bool, update_fields: List):
        self.task_status = self.CHOICE_TASK_STATUS_COMPLETED
        self.completed_datetime = timezone.now()

        # cache를 이용할 때는 queued, processing 데이터가 없음.
        if not self.queued_datetime:
            self.queued_datetime = self.completed_datetime
            update_fields.append('queued_datetime')

        if not self.processing_datetime:
            self.processing_datetime = self.completed_datetime
            update_fields.append('processing_datetime')

        if save:
            self.save(
                update_fields=update_fields + ['task_status', 'completed_datetime']
            )

    def set_error(self, save: bool, msg: str, update_fields: List):
        self.task_status = self.CHOICE_TASK_STATUS_ERROR
        self.error_datetime = timezone.now()

        # cache를 이용할 때는 queued, processing 데이터가 없음.
        if not self.queued_datetime:
            self.queued_datetime = self.error_datetime
            update_fields.append('queued_datetime')

        if not self.processing_datetime:
            self.processing_datetime = self.error_datetime
            update_fields.append('processing_datetime')

        if save:
            self.save(
                update_fields=update_fields + ['task_status', 'error_datetime']
            )

    def set_processing(self, save: bool, update_fields: List):
        self.task_status = self.CHOICE_TASK_STATUS_PROGRESSING
        self.processing_datetime = timezone.now()

        if not self.queued_datetime:
            self.queued_datetime = self.processing_datetime
            update_fields.append('queued_datetime')

        if save:
            self.save(
                update_fields=update_fields + ['task_status', 'processing_datetime']
            )

    @property
    def is_queued_task(self):
        return self.task_status == self.CHOICE_TASK_STATUS_QUEUED

    @property
    def is_processing_task(self):
        return self.task_status == self.CHOICE_TASK_STATUS_PROGRESSING

    @property
    def is_error_task(self):
        return self.task_status == self.CHOICE_TASK_STATUS_ERROR

    @property
    def is_completed_task(self):
        return self.task_status == self.CHOICE_TASK_STATUS_COMPLETED

    @property
    def task_badge_class(self):
        mapping = {
            self.CHOICE_TASK_STATUS_QUEUED: 'bg-secondary',
            self.CHOICE_TASK_STATUS_PROGRESSING: 'bg-info',
            self.CHOICE_TASK_STATUS_ERROR: 'bg-danger',
            self.CHOICE_TASK_STATUS_COMPLETED: 'bg-success',
        }
        return mapping.get(self.task_status, '')

    class Meta:
        abstract = True


class CoordinateMixin(models.Model):

    longitude = models.DecimalField(_('longitude'), max_digits=30, decimal_places=10, null=False, blank=True, default=Decimal('0.0'))
    latitude = models.DecimalField(_('latitude'), max_digits=30, decimal_places=10, null=False, blank=True, default=Decimal('0.0'))

    class Meta:
        abstract = True

    @property
    def is_valid_coordinate(self) -> bool:
        # 124 – 132, 33 – 43
        if self.longitude and self.latitude and (124 - 1 <= self.longitude <= 132 + 1) and (33 - 1 <= self.latitude <= 43 + 1):
            return True
        return False
