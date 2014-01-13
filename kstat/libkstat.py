import ctypes as C

KSTAT_TYPE_RAW   = 0
KSTAT_TYPE_NAMED = 1
KSTAT_TYPE_INTR  = 2
KSTAT_TYPE_IO    = 3
KSTAT_TYPE_TIMER = 4

kstat_type_names = {
    KSTAT_TYPE_RAW:     'raw',
    KSTAT_TYPE_NAMED:   'named',
    KSTAT_TYPE_INTR:    'intr',
    KSTAT_TYPE_IO:      'io',
    KSTAT_TYPE_TIMER:   'timer'
}

KSTAT_STRLEN = 31

hrtime_t     = C.c_longlong
kid_t        = C.c_int
kstat_string = C.c_char * KSTAT_STRLEN

class kstat(C.Structure):
    pass

kstat_p = C.POINTER(kstat)

kstat._fields_ = [
    ('ks_crtime', hrtime_t),
    ('ks_next', kstat_p),
    ('ks_kid', kid_t),
    ('ks_module', kstat_string),
    ('ks_resv', C.c_ubyte),
    ('ks_instance', C.c_int),
    ('ks_name', kstat_string),
    ('ks_type', C.c_ubyte),
    ('ks_class', kstat_string),
    ('ks_flags', C.c_ubyte),
    ('ks_data', C.c_void_p),
    ('ks_ndata', C.c_uint),
    ('ks_data_size', C.c_size_t),
    ('ks_snaptime', hrtime_t),
    ('ks_update', C.c_void_p),
    ('ks_private', C.c_void_p),
    ('ks_snapshot', C.c_void_p),
    ('ks_lock', C.c_void_p)
]

class kstat_ctl(C.Structure):
    _fields_ = [
        ('kc_chain_id', kid_t),
        ('kc_chain', kstat_p),
        ('kc_kd', C.c_int)
    ]

KSTAT_DATA_CHAR         = 0
KSTAT_DATA_INT32        = 1
KSTAT_DATA_UINT32       = 2
KSTAT_DATA_INT64        = 3
KSTAT_DATA_UINT64       = 4
KSTAT_DATA_STRING       = 9
KSTAT_DATA_LONGLONG     = KSTAT_DATA_INT64
KSTAT_DATA_ULONGLONG    = KSTAT_DATA_UINT64
KSTAT_DATA_FLOAT        = 5
KSTAT_DATA_DOUBLE       = 6

class addr_union(C.Union):
    _fields_ = [
        ('ptr', C.c_char_p),
        ('__pad', C.c_char * 8),
    ]

class str_struct(C.Structure):
    _fields_ = [
        ('addr', addr_union),
        ('len', C.c_uint32),
    ]

class value_union(C.Union):
    _fields_ = [
        ('c', C.c_char * 16),
    	('i32', C.c_int32),
    	('ui32', C.c_uint32),
    	('i64', C.c_int64),
    	('ui64', C.c_uint64),
    ]

class kstat_named(C.Structure):
    _fields_ = [
        ('name', kstat_string),
        ('data_type', C.c_ubyte),
        ('value', value_union),
    ]

_libkstat = C.CDLL('libkstat.so.1')

kstat_ctl_p = C.POINTER(kstat_ctl)

kstat_open = _libkstat.kstat_open
kstat_open.argtypes = []
kstat_open.restype = kstat_ctl_p

kstat_close = _libkstat.kstat_close
kstat_close.argtypes = [kstat_ctl_p]

kstat_read = _libkstat.kstat_read
kstat_read.argtypes = [kstat_ctl_p, kstat_p, C.c_void_p]
kstat_read.restype = kid_t

kstat_write = _libkstat.kstat_write
kstat_write.argtypes = [kstat_ctl_p, kstat_p, C.c_void_p]
kstat_write.restype = kid_t

kstat_chain_update = _libkstat.kstat_chain_update
kstat_chain_update.argtypes = [kstat_ctl_p]
kstat_chain_update.restype = kid_t

kstat_lookup = _libkstat.kstat_lookup
kstat_lookup.argtypes = [kstat_ctl_p, C.c_char_p, C.c_int, C.c_char_p]
kstat_lookup.restype = kstat_p

kstat_data_lookup = _libkstat.kstat_data_lookup
kstat_data_lookup.argtypes = [kstat_p]
kstat_data_lookup.restype = C.c_void_p
