import pytest

from testapp.models import AllFieldModel


def test_dummy_model_without_save():
    ##########################################################
    # precondition

    ##########################################################
    # call function
    dummy = AllFieldModel.dummy(save=False)

    ##########################################################
    # assertion
    assert dummy
    assert dummy.id is None
    assert dummy.booleanfield
    assert dummy.charfield
    assert dummy.datefield
    assert dummy.datetimefield
    assert dummy.decimalfield
    assert dummy.durationfield
    assert dummy.emailfield
    assert dummy.filepathfield
    assert dummy.floatfield
    assert dummy.integerfield
    assert dummy.bigintegerfield
    assert dummy.smallintegerfield
    assert dummy.genericipaddressfield
    assert dummy.positivebigintegerfield
    assert dummy.positiveintegerfield
    assert dummy.positivesmallintegerfield
    assert dummy.slugfield
    assert dummy.textfield
    assert dummy.timefield
    assert dummy.urlfield
    assert dummy.binaryfield
    assert dummy.uuidfield
    assert dummy.compressefield


@pytest.mark.django_db
def test_dummy_model_with_save(multidb):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    dummy = AllFieldModel.dummy(save=True)

    ##########################################################
    # assertion
    assert dummy
    assert dummy.id
    assert dummy.booleanfield
    assert dummy.charfield
    assert dummy.datefield
    assert dummy.datetimefield
    assert dummy.decimalfield
    assert dummy.durationfield
    assert dummy.emailfield
    assert dummy.filepathfield
    assert dummy.floatfield
    assert dummy.integerfield
    assert dummy.bigintegerfield
    assert dummy.smallintegerfield
    assert dummy.genericipaddressfield
    assert dummy.positivebigintegerfield
    assert dummy.positiveintegerfield
    assert dummy.positivesmallintegerfield
    assert dummy.slugfield
    assert dummy.textfield
    assert dummy.timefield
    assert dummy.urlfield
    assert dummy.binaryfield
    assert dummy.uuidfield
    assert dummy.compressefield
