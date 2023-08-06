import warnings
from decimal import Decimal
from typing import Dict, Type

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from gpp.model.exceptions import InvalidTaskStatus


def archive_model(queryset, ARCHIVE_MODEL: Type[models.Model], user_id: int, delete_instance: bool):
    """
        archive model

    :param queryset:
    :param ARCHIVE_MODEL:
    :param user_id:
    :param delete_instance:
    :return:
    """
    archive_list = []
    now = timezone.now()

    for instance in chunk_queryset(queryset=queryset, chunk_size=100):

        data = {
            field.attname: getattr(instance, field.attname)
            for field in instance._meta.fields if hasattr(ARCHIVE_MODEL, field.attname)
        }
        data.update({
            'id': None,
            'old_pk': instance.pk,
            'archive_date': now,
            'archive_user_id': user_id,
        })
        archive_list.append(ARCHIVE_MODEL(**data))

    if archive_list:
        ARCHIVE_MODEL.objects.bulk_create(archive_list, 100)
        if delete_instance:
            queryset.delete()


def restore_model(queryset, SOURCE_MODEL: Type[models.Model], delete_instance: bool):
    """
    :param queryset: Queryset
    :param SOURCE_MODEL:
    :return:
    """
    source_objects = []

    for instance in chunk_queryset(queryset=queryset, chunk_size=100):
        data = {
            field.attname: getattr(instance, field.attname)
            for field in instance._meta.fields if hasattr(SOURCE_MODEL, field.attname)
        }
        for attr in ['archive_date', 'archive_user', 'archive_user_id']:
            data.pop(attr, None)

        src_instance = SOURCE_MODEL(**data)
        src_instance.id = instance.old_pk
        source_objects.append(src_instance)

    if source_objects and SOURCE_MODEL.objects.bulk_create(source_objects, 100):
        if delete_instance:
            queryset.delete()


def get_model_differs(src: models.Model, dest: models.Model) -> Dict[str, tuple]:
    """
        src 기준 dest 모델과의 차이
    Args:
        src:
        dest:

    Returns:

    """
    def convert_python_value(instance, field_name):
        """
        python variable type 으로 변환

        Args:
            instance:
            field_name:

        Returns:

        """
        value = getattr(instance, field_name)

        src_field = instance._meta._forward_fields_map.get(field_name)
        if src_field:
            return src_field.get_prep_value(value)

        return None

    ret = {}

    for field in src._meta.fields:
        field_name = field.attname
        if field_name in ('id', 'pk', 'created', 'modified'):
            continue

        src_value = convert_python_value(instance=src, field_name=field_name)
        dest_value = None

        if hasattr(dest, field_name):
            dest_value = convert_python_value(instance=dest, field_name=field_name)

            if isinstance(dest_value, Decimal):
                src_field = src._meta._forward_fields_map.get(field_name)
                if abs(src_value - dest_value) < 0.1 ** src_field.decimal_places:
                    continue
            elif src_value == dest_value:
                continue

        ret.update({field_name: (src_value, dest_value)})

    return ret


def chunk_queryset(queryset, chunk_size):

    last_pk = None

    while True:

        inner_queryset = queryset.order_by('id')

        if last_pk:
            inner_queryset = inner_queryset.filter(id__gt=last_pk)

        data_list = list(inner_queryset.all()[:chunk_size])

        for row in data_list:
            yield row

        if len(data_list) < chunk_size:
            break

        last_pk = data_list[-1].id


def chunk_list(data, chunk_size):
    if not isinstance(data, list):
        data = list(data)
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def truncate_model(MODEL):

    # allowed only specified model

    allowed_model = getattr(settings, 'TRUNCATE_ALLOWED_LABEL', [])

    app_label = MODEL._meta.app_label or ''
    model_name = MODEL._meta.model_name or ''

    keyword = f'{app_label}.{model_name}'

    if keyword in allowed_model:
        db_alias = MODEL.objects.db
        MODEL.objects.using(db_alias).delete()

        warnings.warn(
            "truncate model (TRUNCATE `[DB Table]`) is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        # if db_alias in connections:
        #     with connections[db_alias].cursor() as cursor:
        #         cursor.execute(
        #             'TRUNCATE TABLE `{table}`'.format(table=MODEL._meta.db_table)
        #         )
        #         return True

    return False


def check_task_status(MODEL: Type[models.Model], pk: int):
    """
        MODEL class의 pk를 row-level lock 상태로 load 후,

        status 체크.

    Args:
        MODEL:
        pk:

    Returns:

    """
    db_alias = MODEL.objects.db
    with transaction.atomic(using=db_alias):
        version = MODEL.objects.filter(id=pk).select_for_update().first()

        if version.is_processing_task:
            raise InvalidTaskStatus(version.CHOICE_TASK_STATUS_QUEUED, version.task_status)

        version.set_processing(save=True, update_fields=[])

        return version
