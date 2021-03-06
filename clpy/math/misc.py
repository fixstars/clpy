from clpy import core


# TODO(okuta): Implement convolve


def clip(a, a_min, a_max, out=None):
    """Clips the values of an array to a given interval.

    This is equivalent to ``maximum(minimum(a, a_max), a_min)``, while this
    function is more efficient.

    Args:
        a (clpy.ndarray): The source array.
        a_min (scalar or clpy.ndarray): The left side of the interval.
        a_max (scalar or clpy.ndarray): The right side of the interval.
        out (clpy.ndarray): Output array.

    Returns:
        clpy.ndarray: Clipped array.

    .. seealso:: :func:`numpy.clip`

    """
    # TODO(okuta): check type
    return a.clip(a_min, a_max, out=out)


# sqrt_fixed is deprecated.
# numpy.sqrt is fixed in numpy 1.11.2.
sqrt = sqrt_fixed = core.sqrt


square = core.create_ufunc(
    'clpy_square',
    ('b->b', 'B->B', 'h->h', 'H->H', 'i->i', 'I->I', 'l->l', 'L->L', 'q->q',
     'Q->Q', 'f->f', 'd->d'),
    'out0 = in0 * in0',
    doc='''Elementwise square function.

    .. seealso:: :data:`numpy.square`

    ''')


absolute = core.absolute


# TODO(beam2d): Implement it
# fabs


_unsigned_sign = 'out0 = in0 > 0'
sign = core.create_ufunc(
    'clpy_sign',
    ('b->b', ('B->B', _unsigned_sign), 'h->h', ('H->H', _unsigned_sign),
     'i->i', ('I->I', _unsigned_sign), 'l->l', ('L->L', _unsigned_sign),
     'q->q', ('Q->Q', _unsigned_sign), 'f->f', 'd->d'),
    'out0 = (in0 > 0) - (in0 < 0)',
    doc='''Elementwise sign function.

    It returns -1, 0, or 1 depending on the sign of the input.

    .. seealso:: :data:`numpy.sign`

    ''')


_float_maximum = \
    'out0 = isnan(in0) ? in0 : isnan(in1) ? in1 : fmax(in0, in1)'
maximum = core.create_ufunc(
    'clpy_maximum',
    ('??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H', 'ii->i', 'II->I', 'll->l',
     'LL->L', 'qq->q', 'QQ->Q',
     ('ff->f', _float_maximum),
     ('dd->d', _float_maximum)),
    'out0 = max(in0, in1)',
    doc='''Takes the maximum of two arrays elementwise.

    If NaN appears, it returns the NaN.

    .. seealso:: :data:`numpy.maximum`

    ''')


_float_minimum = \
    'out0 = isnan(in0) ? in0 : isnan(in1) ? in1 : fmin(in0, in1)'
minimum = core.create_ufunc(
    'clpy_minimum',
    ('??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H', 'ii->i', 'II->I', 'll->l',
     'LL->L', 'qq->q', 'QQ->Q',
     ('ff->f', _float_minimum),
     ('dd->d', _float_minimum)),
    'out0 = min(in0, in1)',
    doc='''Takes the minimum of two arrays elementwise.

    If NaN appears, it returns the NaN.

    .. seealso:: :data:`numpy.minimum`

    ''')


_float_fmax = 'out0 = fmax(in0, in1)'
fmax = core.create_ufunc(
    'clpy_fmax',
    ('??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H', 'ii->i', 'II->I', 'll->l',
     'LL->L', 'qq->q', 'QQ->Q',
     ('ff->f', _float_fmax),
     ('dd->d', _float_fmax)),
    'out0 = max(in0, in1)',
    doc='''Takes the maximum of two arrays elementwise.

    If NaN appears, it returns the other operand.

    .. seealso:: :data:`numpy.fmax`

    ''')


_float_fmin = 'out0 = fmin(in0, in1)'
fmin = core.create_ufunc(
    'clpy_fmin',
    ('??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H', 'ii->i', 'II->I', 'll->l',
     'LL->L', 'qq->q', 'QQ->Q',
     ('ff->f', _float_fmin),
     ('dd->d', _float_fmin)),
    'out0 = min(in0, in1)',
    doc='''Takes the minimum of two arrays elementwise.

    If NaN appears, it returns the other operand.

    .. seealso:: :data:`numpy.fmin`

    ''')


# TODO(okuta): Implement nan_to_num


# TODO(okuta): Implement real_if_close


# TODO(okuta): Implement interp
