# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _py_interop_comm
else:
    import _py_interop_comm

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _py_interop_comm.delete_SwigPyIterator

    def value(self):
        return _py_interop_comm.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _py_interop_comm.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _py_interop_comm.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _py_interop_comm.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _py_interop_comm.SwigPyIterator_equal(self, x)

    def copy(self):
        return _py_interop_comm.SwigPyIterator_copy(self)

    def next(self):
        return _py_interop_comm.SwigPyIterator_next(self)

    def __next__(self):
        return _py_interop_comm.SwigPyIterator___next__(self)

    def previous(self):
        return _py_interop_comm.SwigPyIterator_previous(self)

    def advance(self, n):
        return _py_interop_comm.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _py_interop_comm.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _py_interop_comm.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _py_interop_comm.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _py_interop_comm.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _py_interop_comm.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _py_interop_comm.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _py_interop_comm:
_py_interop_comm.SwigPyIterator_swigregister(SwigPyIterator)
import interop.py_interop_run
import interop.py_interop_metrics
class format_exception(interop.py_interop_run.base_exception):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, mesg):
        _py_interop_comm.format_exception_swiginit(self, _py_interop_comm.new_format_exception(mesg))

    def __str__(self):
        return _py_interop_comm.format_exception___str__(self)
    __swig_destroy__ = _py_interop_comm.delete_format_exception

# Register format_exception in _py_interop_comm:
_py_interop_comm.format_exception_swigregister(format_exception)
class file_not_found_exception(interop.py_interop_run.base_exception):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, mesg):
        _py_interop_comm.file_not_found_exception_swiginit(self, _py_interop_comm.new_file_not_found_exception(mesg))

    def __str__(self):
        return _py_interop_comm.file_not_found_exception___str__(self)
    __swig_destroy__ = _py_interop_comm.delete_file_not_found_exception

# Register file_not_found_exception in _py_interop_comm:
_py_interop_comm.file_not_found_exception_swigregister(file_not_found_exception)
class bad_format_exception(format_exception):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, mesg):
        _py_interop_comm.bad_format_exception_swiginit(self, _py_interop_comm.new_bad_format_exception(mesg))

    def __str__(self):
        return _py_interop_comm.bad_format_exception___str__(self)
    __swig_destroy__ = _py_interop_comm.delete_bad_format_exception

# Register bad_format_exception in _py_interop_comm:
_py_interop_comm.bad_format_exception_swigregister(bad_format_exception)
class incomplete_file_exception(format_exception):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, mesg):
        _py_interop_comm.incomplete_file_exception_swiginit(self, _py_interop_comm.new_incomplete_file_exception(mesg))

    def __str__(self):
        return _py_interop_comm.incomplete_file_exception___str__(self)
    __swig_destroy__ = _py_interop_comm.delete_incomplete_file_exception

# Register incomplete_file_exception in _py_interop_comm:
_py_interop_comm.incomplete_file_exception_swigregister(incomplete_file_exception)
class invalid_argument(interop.py_interop_run.base_exception):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, mesg):
        _py_interop_comm.invalid_argument_swiginit(self, _py_interop_comm.new_invalid_argument(mesg))

    def __str__(self):
        return _py_interop_comm.invalid_argument___str__(self)
    __swig_destroy__ = _py_interop_comm.delete_invalid_argument

# Register invalid_argument in _py_interop_comm:
_py_interop_comm.invalid_argument_swigregister(invalid_argument)
class paths(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    @staticmethod
    def run_info(*args):
        return _py_interop_comm.paths_run_info(*args)

    @staticmethod
    def run_parameters(*args):
        return _py_interop_comm.paths_run_parameters(*args)

    @staticmethod
    def rta_config(*args):
        return _py_interop_comm.paths_rta_config(*args)

    @staticmethod
    def interop_filename(run_directory, prefix, suffix, cycle, use_out=True):
        return _py_interop_comm.paths_interop_filename(run_directory, prefix, suffix, cycle, use_out)

    def __init__(self):
        _py_interop_comm.paths_swiginit(self, _py_interop_comm.new_paths())
    __swig_destroy__ = _py_interop_comm.delete_paths

# Register paths in _py_interop_comm:
_py_interop_comm.paths_swigregister(paths)

def is_corrected_intensity_metric_deprecated(version):
    return _py_interop_comm.is_corrected_intensity_metric_deprecated(version)

def is_error_metric_deprecated(version):
    return _py_interop_comm.is_error_metric_deprecated(version)

def is_extended_tile_metric_deprecated(version):
    return _py_interop_comm.is_extended_tile_metric_deprecated(version)

def is_extraction_metric_deprecated(version):
    return _py_interop_comm.is_extraction_metric_deprecated(version)

def is_image_metric_deprecated(version):
    return _py_interop_comm.is_image_metric_deprecated(version)

def is_q_metric_deprecated(version):
    return _py_interop_comm.is_q_metric_deprecated(version)

def is_tile_metric_deprecated(version):
    return _py_interop_comm.is_tile_metric_deprecated(version)

def is_index_metric_deprecated(version):
    return _py_interop_comm.is_index_metric_deprecated(version)

def is_q_collapsed_metric_deprecated(version):
    return _py_interop_comm.is_q_collapsed_metric_deprecated(version)

def is_q_by_lane_metric_deprecated(version):
    return _py_interop_comm.is_q_by_lane_metric_deprecated(version)

def compute_buffer_size(*args):
    return _py_interop_comm.compute_buffer_size(*args)

def write_interop_to_buffer(*args):
    return _py_interop_comm.write_interop_to_buffer(*args)

def read_interop_from_buffer(*args):
    return _py_interop_comm.read_interop_from_buffer(*args)

def read_interop(*args):
    return _py_interop_comm.read_interop(*args)

def write_interop(*args):
    return _py_interop_comm.write_interop(*args)

def read_interop_by_cycle(*args):
    return _py_interop_comm.read_interop_by_cycle(*args)

def is_summary_run_metric_deprecated(version):
    return _py_interop_comm.is_summary_run_metric_deprecated(version)

