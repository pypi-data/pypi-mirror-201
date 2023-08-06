'''
Variable classes. Extends the existing variable types defined in `tkinter`.
'''
import typing
import tkinter as tk
from functools import wraps
from abc import ABCMeta

from . import spec as tkmilan_spec
from . import model as tkmilan_model
if typing.TYPE_CHECKING:
    from . import mixin as tkmilan_mixin
    from . import RootWindow

Variable = tk.Variable

Boolean = tk.BooleanVar
'''Value holder for `bool`.'''
Double = tk.DoubleVar
'''Value holder for `float`.'''
Int = tk.IntVar
'''Value holder for `int`.'''
String = tk.StringVar
'''Value holder for `str`.'''

objT = typing.TypeVar('objT')
'''Generic Type-Checking variable type for `ObjectList`.'''


def trace(var: Variable, function: typing.Callable, *,
          trace_mode: tkmilan_model.TraceModeT = 'write',
          trace_initial: bool = False,
          **kwargs: typing.Any) -> str:
    '''Trace the variable ``var``.

    There is no Python documentation, see ``Tk`` `trace variable <https://www.tcl.tk/man/tcl/TclCmd/trace.html#M14>`_ documentation.

    The ``function`` arguments will be:

      - ``var``: The traced variable
      - ``etype``: The trace mode (see ``trace_mode``)
      - The other given ``kwargs``

    It is possible to run the function as soon as the trace is defined. This is
    useful if the trace is used to keep state in sync.

    Args:
        var: The traced variable.
        function: The callback function.
        trace_mode: The trace mode, when should the callback be invoked.
            `None` when running on the initial function call (see ``trace_initial``).
        trace_initial: Run the callback function on start.
            Runs async (similar to `model.TimeoutIdle`).
        kwargs: Passed to the callback function.

    Returns:
        Return the function identifier, as stored by ``Tk``.
    '''
    assert not isinstance(var, nothing), f'{var}: Tracing "nothing" is unsupported'

    @wraps(function)
    def trace_wrapper(name: str, index: str, etype: str):  # "Real" tk function
        assert isinstance(name, str) and isinstance(etype, str)
        if __debug__:
            assert etype in ['read', 'write', 'unset'], f'Unsupported trace mode: {etype}'
            etype = typing.cast(tkmilan_model.TraceModeT, etype)
        return function(var, etype, **kwargs)

    if trace_initial:
        assert hasattr(var, '_root'), f'Invalid variable object: {var!r}'

        @wraps(function)
        def trace_wrapper_initial():
            return function(var, None, **kwargs)

        rw: 'RootWindow' = var._root
        rw.after_idle(trace_wrapper_initial)  # No need for a `model.TimeoutIdle` here
    return var.trace_add(
        trace_mode,
        trace_wrapper,
    )


class VariableSpecced(Variable, metaclass=ABCMeta):
    '''Base class for variables with a specification.

    This is an `abc`, which means this cannot be instanced directly. This only
    includes the common code for its subclasses.

    Arguments:
        spec: Countable specification of all valid values for the variable.

    All other arguments are passed to the parent constructor.

    See Also:
        Use a regular variable when there's no specification.
    '''
    spec: tkmilan_spec.SpecCountable

    def __init__(self, master=None, value=None, name=None, *, spec: tkmilan_spec.SpecCountable):
        super().__init__(master, value, name)
        self.spec = spec
        assert '' not in self.spec.all(), '{self}: Invalid spec includes empty string'

    # TODO: Implement this? Combined with the "unset" function?
    # def get(self):
    #     value = super().get()
    #     return value if value != '' else None

    # TODO: This could be a common `Variable` method?
    def setDefault(self) -> None:
        '''Set the variable state to the default label on the specification.'''
        self.set(self.spec.default)

    # TODO: Implement `eSet`? Must be `typing.Generic`


class nothing(tk.Variable):
    '''Value holder for `None`.

    Useful for widgets that don't store anything, like buttons.
    '''
    def get(self):
        return None

    def set(self, value: None):
        pass


class aggregator(Variable):
    '''Synthetic value holder for an aggregation of other variables.

    Useful for container widgets.
    '''
    _default: str = ''
    tout: typing.Optional[tkmilan_model.TimeoutIdle]
    '''Hold the `TimeoutIdle <model.TimeoutIdle>` object that indicates
    this variable is setup.

    Since this variable is a synthetic variable, useful only when triggered
    from other function, it needs configuration before it can be used. For
    optimisation reasons, this is not done right on ``__init__`` like most
    other variables.

    Defaults to `None`, indicating it is not ready. See `ready`.
    '''
    # TODO: Save the child variables? `children: typing.Set[Variable]`
    def __init__(self, master=None, value=None, name=None, *, cwidget: 'tkmilan_mixin.MixinWidget'):
        super().__init__(master, value, name)
        self.tout = None
        self.cwidget = cwidget

    @property
    def ready(self) -> bool:
        '''Check if the variable is ready for usage.'''
        return self.tout is not None

    def get(self) -> None:
        assert self.ready, f'{self}: Unprepared aggregator variable'
        super().get()  # Trigger variable read
        return None

    def set(self, value: None = None):
        assert self.ready, f'{self}: Unprepared aggregator variable'
        return super().set('')  # Trigger variable write


# TODO: Support a StringTuple too/instead?
# TODO: Migrate to concrete ObjectList subclass?
class StringList(tk.Variable):
    '''Value holder for `list` of `str`.

    In ``Tk``, everything is a string and the syntax for lists is similar to
    Python, so this is technically supported, but sounds like a coincidence.
    A `list` of non-`str` might be technically supported, but it's untested.

    Works well, though.


    See Also:
        `ObjectList` for an arbitrary list of Python objects.
    '''
    _default: typing.Iterable = []

    def get(self) -> typing.Iterable[str]:
        return [x for x in super().get()]

    def set(self, value: typing.Iterable[str]) -> None:
        return super().set([x for x in value])


class Dict(tk.Variable):
    '''Value holder for dictionary variables.

    Supporting dictionaries on ``Tk`` is probably technically possible, but too
    finicky.

    Just keep an instance variable with the "actual" value. Pretend the value
    is just an empty `str`.
    '''
    # The dummy read/writes are necessary for traces to work correctly
    _default: typing.Mapping = {}
    __actual_value: typing.Optional[typing.Mapping] = None

    def get(self) -> typing.Mapping:
        super().get()  # Dummy read
        return self.__actual_value or dict(self._default)

    def set(self, value: typing.Mapping) -> None:
        self.__actual_value = dict(value)
        return super().set('')  # Dummy write


class ObjectList(tk.Variable, typing.Generic[objT]):
    '''Generic value holder for a sequence of object of `objT` type.

    Just keep an instance variable with the "actual" value. Pretend the value
    is just an empty `str`.

    See Also:
        `StringList`: Similar to this, but for only for strings.
    '''
    # TODO: Write `StringList` as a subclass of this
    # The dummy read/writes are necessary for traces to work correctly
    _default: typing.Sequence[objT] = []
    __actual_value: typing.Optional[typing.Sequence[objT]] = None

    def get(self) -> typing.Sequence[objT]:
        super().get()  # Dummy read
        return self.__actual_value or list(self._default)

    def set(self, value: typing.Sequence[objT]) -> None:
        self.__actual_value = value
        return super().set('')  # Dummy write


class SpeccedString(VariableSpecced, String):
    '''Value holder for `String` variables, with a specification.

    This is like a regular `String`, with an extra argument that contains a
    specification of possible values.
    '''
    pass
