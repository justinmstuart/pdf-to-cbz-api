from utils.errors import create_error_response


def test_create_error_response_structure():
    body, code = create_error_response('Something went wrong', 400)
    assert body == {'error': 'Something went wrong'}
    assert code == 400


def test_create_error_response_500():
    body, code = create_error_response('Internal error', 500)
    assert body == {'error': 'Internal error'}
    assert code == 500


def test_create_error_response_preserves_message():
    message = 'Specific error detail'
    body, _ = create_error_response(message, 422)
    assert body['error'] == message
