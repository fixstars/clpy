from clpy.backend cimport device
cimport clpy.backend.opencl.api
from clpy.backend.opencl.types cimport cl_mem

cdef class Buf:
    cdef cl_mem ptr
    cpdef size_t get(self)

cdef class Chunk:

    cdef:
        readonly device.Device device
        readonly object mem
        readonly Buf buf
        readonly Py_ssize_t offset
        readonly Py_ssize_t size
        public Chunk prev
        public Chunk next
        public bint in_use

cdef class MemoryPointer:

    cdef:
        readonly device.Device device
        readonly object mem
        readonly Buf buf
        readonly Py_ssize_t offset

    cpdef copy_from_device(self, MemoryPointer src, Py_ssize_t size)
    cpdef copy_from_device_async(self, MemoryPointer src, size_t size, stream)
    cpdef copy_from_host(self, mem, size_t size)
    cpdef copy_from_host_async(self, mem, size_t size, stream)
    cpdef copy_from(self, mem, size_t size)
    cpdef copy_from_async(self, mem, size_t size, stream)
    cpdef copy_to_host(self, mem, size_t size)
    cpdef copy_to_host_async(self, mem, size_t size, stream)
    cpdef memset(self, int value, size_t size)
    cpdef memset_async(self, int value, size_t size, stream)
    cpdef Py_ssize_t cl_mem_offset(self)


cpdef is_allocator_default()
cpdef MemoryPointer alloc(Py_ssize_t size)
cpdef MemoryPointer malloc_zerocopy(Py_ssize_t size)

cpdef set_allocator(allocator=*)


cdef class SingleDeviceMemoryPool:

    cdef:
        object _allocator
        dict _in_use
        list _free
        object __weakref__
        object _weakref
        object _free_lock
        object _in_use_lock
        readonly Py_ssize_t _allocation_unit_size
        readonly Py_ssize_t _initial_bins_size
        readonly int _device_id

    cpdef MemoryPointer _alloc(self, Py_ssize_t size)
    cpdef MemoryPointer malloc(self, Py_ssize_t size)
    cpdef MemoryPointer _malloc(self, Py_ssize_t size)
    cpdef free(self, Buf buf, Py_ssize_t size, Py_ssize_t offset)
    cpdef free_all_blocks(self)
    cpdef free_all_free(self)
    cpdef n_free_blocks(self)
    cpdef used_bytes(self)
    cpdef free_bytes(self)
    cpdef total_bytes(self)
    cpdef Py_ssize_t _round_size(self, Py_ssize_t size)
    cpdef Py_ssize_t _bin_index_from_size(self, Py_ssize_t size)
    cpdef void _grow_free_if_necessary(self, Py_ssize_t size)
    cpdef tuple _split(self, Chunk chunk, Py_ssize_t size)
    cpdef Chunk _merge(self, Chunk head, Chunk remaining)

cdef class MemoryPool:

    cdef:
        object _pools

    cpdef MemoryPointer malloc(self, Py_ssize_t size)
    cpdef free_all_blocks(self)
    cpdef free_all_free(self)
    cpdef n_free_blocks(self)
    cpdef used_bytes(self)
    cpdef free_bytes(self)
    cpdef total_bytes(self)
