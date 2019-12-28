from sage.numerical.backends.generic_backend cimport GenericBackend

cdef class TestBackend(GenericBackend):
    cpdef add_col(self, indices, coeffs):
        pass


