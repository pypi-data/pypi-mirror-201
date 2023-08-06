from tera_etl.utils.normalise_utils import assign_to_event, clean_email_field, clean_phone_field


def test_assign_to_event():
    event_object = {}
    assign_to_event(event_object, 'CrmId', 'CrmId')
    assert 'CrmId' == event_object['CrmId']

    assert assign_to_event(event_object, 'Email', '') is None


def test_clean_email_field():
    assert clean_email_field('') is None
    assert clean_email_field('vtvcab@vtvcab.vn') is None
    assert clean_email_field('test_mail@gmail.com') == 'test_mail@gmail.com'
    assert clean_email_field('test_mail@@gmail.com') is None
    assert clean_email_field('test/mail@gmail.com') == 'mail@gmail.com'


def test_clean_phone_field():
    assert clean_phone_field('') is None
    assert clean_phone_field('123456789191923828312832188') is None
    assert clean_phone_field('3712240') is None
    
    assert clean_phone_field('935449999') == '84935449999'
    assert clean_phone_field('0935449999') == '84935449999'
    assert clean_phone_field('00840935449999') == '84935449999'
    assert clean_phone_field('0840935449999') == '84935449999'
    assert clean_phone_field('840935449999') == '84935449999'
    assert clean_phone_field('84935449999') == '84935449999'

    assert clean_phone_field('1635449999') == '84335449999'
    assert clean_phone_field('01635449999') == '84335449999'
    assert clean_phone_field('008401635449999') == '84335449999'
    assert clean_phone_field('08401635449999') == '84335449999'
    assert clean_phone_field('8401635449999') == '84335449999'
    assert clean_phone_field('841635449999') == '84335449999'
