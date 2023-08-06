import pytest
from django.test import override_settings

from gpp.model.exceptions import InvalidTaskStatus
from gpp.model.utils import archive_model, restore_model, get_model_differs, truncate_model, chunk_queryset, \
    chunk_list, check_task_status
from testapp.models import AllFieldModel, ArchivedAllFieldModel, TaskModel


@pytest.mark.django_db
def test_django_model_archive(multidb):
    ##########################################################
    # precondition
    dummy = AllFieldModel.dummy(save=True)

    ##########################################################
    # assertion
    assert AllFieldModel.objects.count() == 1
    assert ArchivedAllFieldModel.objects.count() == 0

    ##########################################################
    # backup
    archive_model(
        queryset=AllFieldModel.objects.all(),
        ARCHIVE_MODEL=ArchivedAllFieldModel,
        user_id=1,
        delete_instance=True,
    )

    ##########################################################
    # assertion
    assert AllFieldModel.objects.count() == 0
    assert ArchivedAllFieldModel.objects.count() == 1

    archive = ArchivedAllFieldModel.objects.first()
    assert not get_model_differs(dummy, archive)

    ##########################################################
    # restore
    restore_model(
        queryset=ArchivedAllFieldModel.objects.filter(old_pk=dummy.id).all(),
        SOURCE_MODEL=AllFieldModel,
        delete_instance=True
    )

    ##########################################################
    # assertion
    assert AllFieldModel.objects.count() == 1
    assert ArchivedAllFieldModel.objects.count() == 0

    new_instance = AllFieldModel.objects.first()
    assert not get_model_differs(dummy, new_instance)


@pytest.mark.django_db
def test_django_chunk_queryset(multidb):
    ##########################################################
    # precondition
    AllFieldModel.objects.bulk_create(
        AllFieldModel.dummy(id=i, save=False) for i in range(1, 10 + 1)
    )

    ret = []
    queryset = AllFieldModel.objects.filter(id__in=[2, 3, 4])

    ##########################################################
    # call function
    for row in chunk_queryset(queryset=queryset, chunk_size=1):
        ret.append(row.id)

    ##########################################################
    # assertion
    assert ret
    assert set(ret) == {2, 3, 4}


def test_django_truncate_list():
    ##########################################################
    # precondition
    data = [i for i in range(1, 20 + 1)]

    ##########################################################
    # call function
    loop = chunk_list(data=data, chunk_size=7)

    ##########################################################
    # assertion
    assert next(loop) == [1, 2, 3, 4, 5, 6, 7]
    assert next(loop) == [8, 9, 10, 11, 12, 13, 14]
    assert next(loop) == [15, 16, 17, 18, 19, 20]

    with pytest.raises(StopIteration):
        next(loop)

    ##########################################################
    # call function
    loop = chunk_list(data=data, chunk_size=20)

    ##########################################################
    # assertion
    assert next(loop) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    with pytest.raises(StopIteration):
        next(loop)

    ##########################################################
    # call function
    loop = chunk_list(data=data, chunk_size=100)

    ##########################################################
    # assertion
    assert next(loop) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    with pytest.raises(StopIteration):
        next(loop)


@override_settings(TRUNCATE_ALLOWED_LABEL={'testapp.allfieldmodel', })
@pytest.mark.django_db
def test_truncate_model():
    ##########################################################
    # precondition
    AllFieldModel.dummy(save=True)

    ##########################################################
    # assertion
    assert AllFieldModel.objects.count() == 1

    ##########################################################
    # call function
    truncate_model(MODEL=AllFieldModel)

    ##########################################################
    # assertion
    assert AllFieldModel.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('task_status', [
    TaskModel.CHOICE_TASK_STATUS_QUEUED,
    TaskModel.CHOICE_TASK_STATUS_ERROR,
    TaskModel.CHOICE_TASK_STATUS_COMPLETED,
])
def test_django_check_task_status_valid(multidb, task_status):
    ##########################################################
    # precondition
    task = TaskModel.dummy(save=True, task_status=task_status)

    ##########################################################
    # call function
    new_instance = check_task_status(MODEL=TaskModel, pk=task.id)

    assert new_instance.is_processing_task


@pytest.mark.django_db
@pytest.mark.parametrize('task_status', [
    TaskModel.CHOICE_TASK_STATUS_PROGRESSING,
])
def test_django_check_task_status_exception(multidb, task_status):
    ##########################################################
    # precondition
    task = TaskModel.dummy(save=True, task_status=task_status)

    ##########################################################
    # call function
    with pytest.raises(InvalidTaskStatus):
        check_task_status(MODEL=TaskModel, pk=task.id)


@pytest.mark.django_db
@pytest.mark.parametrize('task_status, is_queued, is_processing, is_error, is_completed', [
    (TaskModel.CHOICE_TASK_STATUS_QUEUED, True, False, False, False),
    (TaskModel.CHOICE_TASK_STATUS_PROGRESSING, False, True, False, False),
    (TaskModel.CHOICE_TASK_STATUS_ERROR, False, False, True, False),
    (TaskModel.CHOICE_TASK_STATUS_COMPLETED, False, False, False, True),
])
def test_django_check_task_status_properties(multidb, task_status, is_queued, is_processing, is_error, is_completed):
    ##########################################################
    # precondition
    task = TaskModel.dummy(save=True, task_status=task_status)

    ##########################################################
    # assertion
    assert task.is_queued_task == is_queued
    assert task.is_processing_task == is_processing
    assert task.is_error_task == is_error
    assert task.is_completed_task == is_completed
    assert task.task_badge_class


@pytest.mark.django_db
def test_django_check_task_each_set_functions(multidb):
    ##########################################################
    # precondition
    TaskModel.objects.create(task_status=TaskModel.CHOICE_TASK_STATUS_QUEUED)

    ##########################################################
    # assertion
    task: TaskModel = TaskModel.objects.first()
    assert task.is_queued_task
    task.delete()

    TaskModel.objects.create(task_status=TaskModel.CHOICE_TASK_STATUS_QUEUED)
    task: TaskModel = TaskModel.objects.first()
    task.set_error(save=True, update_fields=[], msg='')
    assert task.is_error_task
    assert task.error_datetime
    task.delete()
    TaskModel.objects.create(task_status=TaskModel.CHOICE_TASK_STATUS_QUEUED)

    task: TaskModel = TaskModel.objects.first()
    task.set_processing(save=True, update_fields=[])
    assert task.is_processing_task
    assert task.processing_datetime
    task.delete()

    TaskModel.objects.create(task_status=TaskModel.CHOICE_TASK_STATUS_QUEUED)
    task: TaskModel = TaskModel.objects.first()
    task.set_completed(save=True, update_fields=[])
    assert task.is_completed_task
    assert task.completed_datetime
