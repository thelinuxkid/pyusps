def assert_raises(excClass, callableObj, *args, **kwargs):
    """
    Like unittest.TestCase.assertRaises, but returns the exception.
    """
    try:
        callableObj(*args, **kwargs)
    except excClass, e:
        return e
    else:
        if hasattr(excClass,'__name__'): excName = excClass.__name__
        else: excName = str(excClass)
        raise AssertionError("%s not raised" % excName)

def assert_errors_equal(error_1, error_2):
    assert type(error_1) == type(error_2)
    assert error_1.message, error_2.message
    assert error_1.args, error_2.args
