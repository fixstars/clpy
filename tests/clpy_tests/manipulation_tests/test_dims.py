import numpy
import unittest

import clpy
from clpy import testing


@testing.gpu
class TestDims(unittest.TestCase):

    _multiprocess_can_split_ = True

    def check_atleast(self, func, xp):
        a = testing.shaped_arange((), xp)
        b = testing.shaped_arange((2,), xp)
        c = testing.shaped_arange((2, 2), xp)
        d = testing.shaped_arange((4, 3, 2), xp)
        return func(a, b, c, d)

    @testing.numpy_clpy_array_list_equal()
    def test_atleast_1d1(self, xp):
        return self.check_atleast(xp.atleast_1d, xp)

    @testing.numpy_clpy_array_equal()
    def test_atleast_1d2(self, xp):
        a = testing.shaped_arange((1, 3, 2), xp)
        return xp.atleast_1d(a)

    @testing.numpy_clpy_array_list_equal()
    def test_atleast_2d1(self, xp):
        return self.check_atleast(xp.atleast_2d, xp)

    @testing.numpy_clpy_array_equal()
    def test_atleast_2d2(self, xp):
        a = testing.shaped_arange((1, 3, 2), xp)
        return xp.atleast_2d(a)

    @testing.numpy_clpy_array_list_equal()
    def test_atleast_3d1(self, xp):
        return self.check_atleast(xp.atleast_3d, xp)

    @testing.numpy_clpy_array_equal()
    def test_atleast_3d2(self, xp):
        a = testing.shaped_arange((1, 3, 2), xp)
        return xp.atleast_3d(a)

    @testing.for_all_dtypes()
    @testing.numpy_clpy_array_equal()
    def test_broadcast_arrays(self, xp, dtype):
        a = testing.shaped_arange((2, 1, 3, 4), xp, dtype)
        b = testing.shaped_arange((3, 1, 4), xp, dtype)
        c, d = xp.broadcast_arrays(a, b)
        return d

    @testing.with_requires('numpy>=1.10')
    @testing.for_all_dtypes()
    @testing.numpy_clpy_array_equal()
    def test_broadcast_to(self, xp, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((3, 1, 4), xp, dtype)
        b = xp.broadcast_to(a, (2, 3, 3, 4))
        return b

    @testing.with_requires('numpy>=1.10')
    @testing.for_all_dtypes()
    @testing.numpy_clpy_raises()
    def test_broadcast_to_fail(self, xp, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((3, 1, 4), xp, dtype)
        xp.broadcast_to(a, (1, 3, 4))

    @testing.with_requires('numpy>=1.10')
    @testing.for_all_dtypes()
    @testing.numpy_clpy_raises()
    def test_broadcast_to_short_shape(self, xp, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((1, 3, 4), xp, dtype)
        xp.broadcast_to(a, (3, 4))

    @testing.for_all_dtypes()
    @testing.numpy_clpy_array_equal()
    def test_broadcast_to_numpy19(self, xp, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((3, 1, 4), xp, dtype)
        if xp is clpy:
            b = xp.broadcast_to(a, (2, 3, 3, 4))
        else:
            dummy = xp.empty((2, 3, 3, 4))
            b, _ = xp.broadcast_arrays(a, dummy)
        return b

    @testing.for_all_dtypes()
    def test_broadcast_to_fail_numpy19(self, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((3, 1, 4), clpy, dtype)
        with self.assertRaises(ValueError):
            clpy.broadcast_to(a, (1, 3, 4))

    @testing.for_all_dtypes()
    def test_broadcast_to_short_shape_numpy19(self, dtype):
        # Note that broadcast_to is only supported on numpy>=1.10
        a = testing.shaped_arange((1, 3, 4), clpy, dtype)
        with self.assertRaises(ValueError):
            clpy.broadcast_to(a, (3, 4))

    @testing.numpy_clpy_array_equal()
    def test_expand_dims0(self, xp):
        a = testing.shaped_arange((2, 3), xp)
        return xp.expand_dims(a, 0)

    @testing.numpy_clpy_array_equal()
    def test_expand_dims1(self, xp):
        a = testing.shaped_arange((2, 3), xp)
        return xp.expand_dims(a, 1)

    @testing.numpy_clpy_array_equal()
    def test_expand_dims2(self, xp):
        a = testing.shaped_arange((2, 3), xp)
        return xp.expand_dims(a, 2)

    @testing.numpy_clpy_array_equal()
    def test_expand_dims_negative1(self, xp):
        a = testing.shaped_arange((2, 3), xp)
        return xp.expand_dims(a, -2)

    @testing.with_requires('numpy>=1.13')
    @testing.numpy_clpy_array_equal()
    def test_expand_dims_negative2(self, xp):
        a = testing.shaped_arange((2, 3), xp)
        # Too large and too small axis is deprecated in NumPy 1.13
        with testing.assert_warns(DeprecationWarning):
            return xp.expand_dims(a, -4)

    @testing.numpy_clpy_array_equal()
    def test_squeeze1(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze()

    @testing.numpy_clpy_array_equal()
    def test_squeeze2(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return a.squeeze()

    @testing.numpy_clpy_array_equal()
    def test_squeeze_int_axis1(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=2)

    @testing.numpy_clpy_array_equal()
    def test_squeeze_int_axis2(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=-3)

    @testing.with_requires('numpy>=1.13')
    @testing.numpy_clpy_raises()
    def test_squeeze_int_axis_failure1(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        a.squeeze(axis=-9)

    def test_squeeze_int_axis_failure2(self):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), clpy)
        with self.assertRaises(clpy.core.core._AxisError):
            a.squeeze(axis=-9)

    @testing.numpy_clpy_array_equal()
    def test_squeeze_tuple_axis1(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=(2, 4))

    @testing.numpy_clpy_array_equal()
    def test_squeeze_tuple_axis2(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=(-4, -3))

    @testing.numpy_clpy_array_equal()
    def test_squeeze_tuple_axis3(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=(4, 2))

    @testing.numpy_clpy_array_equal()
    def test_squeeze_tuple_axis4(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return a.squeeze(axis=())

    @testing.with_requires('numpy>=1.13')
    @testing.numpy_clpy_raises()
    def test_squeeze_tuple_axis_failure1(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        a.squeeze(axis=(-9,))

    @testing.numpy_clpy_raises()
    def test_squeeze_tuple_axis_failure2(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        a.squeeze(axis=(2, 2))

    def test_squeeze_tuple_axis_failure3(self):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), clpy)
        with self.assertRaises(clpy.core.core._AxisError):
            a.squeeze(axis=(-9,))

    @testing.numpy_clpy_array_equal()
    def test_squeeze_scalar1(self, xp):
        a = testing.shaped_arange((), xp)
        return a.squeeze(axis=0)

    @testing.numpy_clpy_array_equal()
    def test_squeeze_scalar2(self, xp):
        a = testing.shaped_arange((), xp)
        return a.squeeze(axis=-1)

    @testing.with_requires('numpy>=1.13')
    @testing.numpy_clpy_raises()
    def test_squeeze_scalar_failure1(self, xp):
        a = testing.shaped_arange((), xp)
        a.squeeze(axis=-2)

    @testing.with_requires('numpy>=1.13')
    @testing.numpy_clpy_raises()
    def test_squeeze_scalar_failure2(self, xp):
        a = testing.shaped_arange((), xp)
        a.squeeze(axis=1)

    def test_squeeze_scalar_failure3(self):
        a = testing.shaped_arange((), clpy)
        with self.assertRaises(clpy.core.core._AxisError):
            a.squeeze(axis=-2)

    def test_squeeze_scalar_failure4(self):
        a = testing.shaped_arange((), clpy)
        with self.assertRaises(clpy.core.core._AxisError):
            a.squeeze(axis=1)

    @testing.numpy_clpy_raises()
    def test_squeeze_failure(self, xp):
        a = testing.shaped_arange((2, 1, 3, 4), xp)
        a.squeeze(axis=2)

    @testing.numpy_clpy_array_equal()
    def test_external_squeeze(self, xp):
        a = testing.shaped_arange((1, 2, 1, 3, 1, 1, 4, 1), xp)
        return xp.squeeze(a)


@testing.parameterize(
    {'shapes': [(), ()]},
    {'shapes': [(0,), (0,)]},
    {'shapes': [(1,), (1,)]},
    {'shapes': [(2,), (2,)]},
    {'shapes': [(0,), (1,)]},
    {'shapes': [(2, 3), (1, 3)]},
    {'shapes': [(2, 1, 3, 4), (3, 1, 4)]},
    {'shapes': [(4, 3, 2, 3), (2, 3)]},
    {'shapes': [(2, 0, 1, 1, 3), (2, 1, 0, 0, 3)]},
    {'shapes': [(0, 1, 1, 3), (2, 1, 0, 0, 3)]},
    {'shapes': [(0, 1, 1, 0, 3), (5, 2, 0, 1, 0, 0, 3), (2, 1, 0, 0, 0, 3)]},
)
@testing.gpu
class TestBroadcast(unittest.TestCase):

    # TODO(niboshi): Run test of xp.broadcast_arrays in this class

    def _broadcast(self, xp, shapes):
        arrays = [
            testing.shaped_arange(s, xp, xp.float32) for s in shapes]
        return xp.broadcast(*arrays)

    def test_broadcast(self):
        broadcast_np = self._broadcast(numpy, self.shapes)
        broadcast_cp = self._broadcast(clpy, self.shapes)
        self.assertEqual(broadcast_np.shape, broadcast_cp.shape)
        self.assertEqual(broadcast_np.size, broadcast_cp.size)
        self.assertEqual(broadcast_np.nd, broadcast_cp.nd)


@testing.parameterize(
    {'shapes': [(3,), (2,)]},
    {'shapes': [(3, 2), (2, 3,)]},
    {'shapes': [(3, 2), (3, 4,)]},
    {'shapes': [(0,), (2,)]},
)
@testing.gpu
class TestInvalidBroadcast(unittest.TestCase):

    # TODO(niboshi): Run test of xp.broadcast_arrays in this class

    @testing.numpy_clpy_raises()
    def test_invalid_broadcast(self, xp):
        arrays = [
            testing.shaped_arange(s, xp, xp.float32) for s in self.shapes]
        xp.broadcast(*arrays)
