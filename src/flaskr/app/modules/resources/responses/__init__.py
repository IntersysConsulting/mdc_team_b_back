from flask import jsonify


def element_does_not_exist(element):
    return jsonify({
        "statusCode": 410,
        'message': 'Requested {} does not exist'.format(element)
    })


def operation_failed(operation):
    return jsonify({
        "statusCode": 500,
        'message': 'Could not {} succesfully.'.format(operation)
    })


def unexpected_result(result):
    return jsonify({
        "statusCode":
        500,
        'message':
        'Server produced an unexpected result: {}.'.format(result)
    })


def change_is_not_valid():
    return jsonify({
        "statusCode": 406,
        'message': 'Requested method can not be used in this way'
    })


def success(operation):
    return jsonify({
        "statusCode": 200,
        'message': '{} was successful.'.format(operation)
    })


def partial_success(operation, partial_error):
    return jsonify({
        "statusCode": 206,
        'message': '{} was successful but {} failed.'.format(operation, partial_error)
    })
