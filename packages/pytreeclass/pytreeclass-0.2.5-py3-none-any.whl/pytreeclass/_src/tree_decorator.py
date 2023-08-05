from __future__ import annotations

import copy
import functools as ft
import sys
from collections import defaultdict
from contextlib import contextmanager
from types import FunctionType, MappingProxyType
from typing import Any, Callable, Mapping, NamedTuple, Sequence, TypeVar

_NOT_SET = type("NOT_SET", (), {"__repr__": lambda _: "?"})()
_MUTABLE_TYPES = (list, dict, set)
_ANNOTATIONS = "__annotations__"
_POST_INIT = "__post_init__"
_MUTABLE = "__mutable__"
T = TypeVar("T")

PyTree = Any


"""Define custom frozen `dataclasses.dataclass`-like decorator"""
# similar to dataclass decorator for init code generation
# the motivation for writing this is to avoid the need to use dataclasses
# especially after this update https://github.com/google/jax/issues/14295
# in essence, after this upadte jax arrays are considred mutable by the field logic


# A registry to store the fields of the `treeclass` wrapped classes. fields are a similar concept to
# `dataclasses.Field` but with the addition of `callbacks` attribute
# While `dataclasses` fields are added as a class attribute to the class under `__dataclass_fields__`
# in this implementation, the fields are stored in a `defaultdict` as an extra precaution
# to avoid user-side modification of the fields while maintaining a cleaner namespace
_field_registry: dict[type, Mapping[str, Field]] = defaultdict(dict)


def register_pytree_field_map(klass: type[T], field_map: Mapping[str, Field]) -> None:
    # register the field map of a class to the registry
    # field map is a mapping of field name to `Field` object
    # the fields are used to generate the `__init__`, `__str__`, `__repr__` functions
    # and to define the leaves in `tree_flatten` and `tree_unflatten` functions
    _field_registry[klass].update(field_map)


def ovars(obj: Any) -> dict[str, Any]:
    """Returns a dictionary of the object's attributes."""
    return object.__getattribute__(obj, "__dict__")


def is_treeclass(item: Any) -> bool:
    """Returns `True` if a class or instance is a `treeclass`."""
    klass = item if isinstance(item, type) else type(item)
    return klass in _field_registry


class Field(NamedTuple):
    # Immutable version of dataclasses.Field
    # with the addition `callbacks` attributes
    name: str | None = None
    type: type | None = None
    default: Any = _NOT_SET
    factory: Any = None
    init: bool = True
    repr: bool = True
    kw_only: bool = False
    pos_only: bool = False
    metadata: MappingProxyType[str, Any] | None = None
    callbacks: Sequence[Any] = ()


def field(
    *,
    default: Any = _NOT_SET,
    factory: Callable | None = None,
    init: bool = True,
    repr: bool = True,
    kw_only: bool = False,
    pos_only: bool = False,
    metadata: dict[str, Any] | None = None,  # type: ignore
    callbacks: Sequence[Any] = (),
) -> Field:
    """
    Args:
        default: The default value of the field. Mutually exclusive with `factory`.
        factory: A 0-argument function called to initialize field value. Mutually exclusive with `default`.
        init: Whether the field is included in the object's __init__ function.
        repr: Whether the field is included in the object's __repr__ function.
        kw_only: Whether the field is keyword-only. Mutually exclusive with `pos_only`.
        pos_only: Whether the field is positional-only. Mutually exclusive with `kw_only`.
        metadata: A mapping of user-defined data for the field.
        callbacks: A sequence of functions to called on `setattr` during initialization to modify the field value.

    Example:
        >>> import pytreeclass as pytc
        >>> @pytc.treeclass
        ... class Foo:
        ...     x: int = pytc.field(callbacks=[lambda x: x + 1])  # value is incremented by 1 after initialization
        >>> foo = Foo(x=1)
        >>> foo.x
        2
    """
    if default is not _NOT_SET and factory is not None:
        # mutually exclusive arguments
        # this is the similar behavior to `dataclasses`
        msg = "`default` and `factory` are mutually exclusive arguments."
        msg += f"got default={default} and factory={factory}"
        raise ValueError(msg)

    if kw_only is True and pos_only is True:
        # mutually exclusive arguments
        msg = "`kw_only` and `pos_only` are mutually exclusive arguments."
        msg += f"got kw_only={kw_only} and pos_only={pos_only}"
        raise ValueError(msg)

    if isinstance(metadata, dict):
        metadata = MappingProxyType(metadata)  # type: ignore
    elif metadata is not None:
        raise TypeError("`metadata` must be a Mapping or None")

    # check if `callbacks` is a Sequence of functions
    if not isinstance(callbacks, Sequence):
        msg = f"`callbacks` must be a Sequence of functions, got {type(callbacks)}"
        raise TypeError(msg)

    # sanity check for callbacks
    for index, callback in enumerate(callbacks):
        if not isinstance(callback, Callable):  # type: ignore
            msg = "`callbacks` must be a Sequence of functions, "
            msg += f"got `{type(callbacks).__name__}` at index={index}"
            raise TypeError(msg)

    # set name and type post initialization
    return Field(
        name=None,
        type=None,
        default=default,
        factory=factory,
        init=init,
        repr=repr,
        kw_only=kw_only,
        pos_only=pos_only,
        metadata=metadata,  # type: ignore
        callbacks=callbacks,
    )


def fields(item: Any) -> Sequence[Field]:
    """Get the fields of a `treeclass` instance."""
    if (klass := item if isinstance(item, type) else type(item)) not in _field_registry:
        raise TypeError(f"Cannot get fields of {item!r}.")

    return tuple(_field_registry[klass].values())


def _generate_field_map(klass: type) -> dict[str, Field]:
    # get all the fields of the class and its base classes
    # get the fields of the class and its base classes
    field_map = dict()

    for base in reversed(klass.__mro__):
        # get the fields of the base class in the MRO
        # in reverse order to ensure the correct order of the fields
        # are preserved, i.e. the fields of the base class are added first
        # and the fields of the derived class are added last so that
        # in case of name collision, the derived class fields are preserved
        if base in _field_registry:
            field_map.update(_field_registry[base])

    # transform the annotated attributes of the class into Fields
    # while assigning the default values of the Fields to the annotated attributes
    # TODO: use inspect to get annotations, once we are on minimum python version >3.9
    if _ANNOTATIONS not in vars(klass):
        return field_map

    for name in (annotation_map := vars(klass)[_ANNOTATIONS]):
        # get the value associated with the type hint
        # in essence will skip any non type-hinted attributes
        value = getattr(klass, name, _NOT_SET)
        # at this point we stick to the type hint provided by the user
        # inconsistency between the type hint and the value will be handled later
        type = annotation_map[name]

        if name == "self":
            # while `dataclasses` allows `self` as a field name, its confusing
            # and not recommended. so raise an error
            msg = "Field name cannot be `self`."
            raise ValueError(msg)

        if isinstance(value, Field):
            # the annotated attribute is a `Field``
            # example case: `x: Any = field(default=1)`
            # assign the name and type to the Field from the annotation
            if isinstance(value.default, _MUTABLE_TYPES):
                # example case: `x: Any = field(default=[1, 2, 3])`
                # https://github.com/ericvsmith/dataclasses/issues/3
                msg = f"Mutable default value of field `{name}` is not allowed, use "
                msg += f"`factory=lambda: {value.default}` instead."
                raise TypeError(msg)

            field_map[name] = value._replace(name=name, type=type)

        elif isinstance(value, _MUTABLE_TYPES):
            # https://github.com/ericvsmith/dataclasses/issues/3
            # example case: `x: Any = [1, 2, 3]`
            # this is the prime motivation for writing this decorator
            # as from python 3.11, jax arrays `dataclasses` will raise an error if
            # `JAX` arrays are used as default values.
            # the `dataclasses` logic is flawed by using `__hash__` existence
            # as a proxy for immutability, which is not the case for `JAX` arrays
            # which are immutable but do not have a `__hash__` method
            msg = f"Mutable value= {(value)} is not allowed"
            msg += f" for field `{name}` in class `{klass.__name__}`.\n"
            msg += f" use `field(... ,factory=lambda:{value})` instead"
            raise TypeError(msg)

        elif value is _NOT_SET:
            # nothing is assigned to the annotated attribute
            # example case: `x: Any`
            # create a Field and assign it to the class
            field_map[name] = Field(name=name, type=type)

        else:
            # example case: `x: int = 1`
            # create a Field and assign default value to the class
            field_map[name] = Field(name=name, type=type, default=value)

    return field_map


@ft.lru_cache
def _generate_init_code(fields: Sequence[Field]):
    # generate the init method code string
    # in here, we generate the function head and body and add `default`/`factory`
    # for example, if we have a class with fields `x` and `y`
    # then generated code will something like  `def __init__(self, x, y): self.x = x; self.y = y`
    head = body = ""

    for field in fields:
        key = field.name

        mark0 = f"field_map['{key}'].default"
        mark1 = f"field_map['{key}'].factory()"
        mark2 = f"self.{key}"

        if field.kw_only and "*" not in head and field.init:
            # if the field is keyword only, and we have not added the `*` yet
            head += "*, "

        if field.default is not _NOT_SET:
            # we add the default into the function head (def f(.. x= default_value))
            # if the the field require initialization. if not, then omit it from head
            head += f"{key}={mark0}, " if field.init else ""
            # we then add self.x = x for the body function if field is initialized
            # otherwise, define the default value inside the body ( self.x = default_value)
            body += f"\t\t{mark2}=" + (f"{key}\n " if field.init else f"{mark0}\n")
        elif field.factory is not None:
            # same story for functions as above
            head += f"{key}={mark1}, " if field.init else ""
            body += f"\t\t{mark2}=" + (f"{key}\n" if field.init else f"{mark1}\n")
        else:
            # no defaults are added
            head += f"{key}, " if field.init else ""
            body += f"\t\t{mark2}={key}\n " if field.init else ""

        if field.pos_only and field.init:
            # if the field is positional only, we add a "/" marker after it
            if "/" in head:
                head = head.replace("/,", "")

            head += "/, "

    # in case no field is initialized, we add a pass statement to the body
    # to avoid syntax error in the generated code
    body += "\t\tpass"
    # add the body to the head
    body = "\tdef __init__(self, " + head[:-2] + "):\n" + body
    # use closure to be able to reference default values of all types
    body = f"def closure(field_map):\n{body}\n\treturn __init__"
    return body.expandtabs(4)


def _generate_init(klass: type) -> FunctionType:
    # generate the field map for the class
    field_map = _generate_field_map(klass)
    # generate init method
    local_namespace = dict()  # type: ignore
    global_namespace = vars(sys.modules[klass.__module__])

    # generate the init method code string
    # in here, we generate the function head and body and add `default`/`factory`
    exec(_generate_init_code(field_map.values()), global_namespace, local_namespace)
    method = local_namespace["closure"](field_map)

    # inject the method into the class namespace
    return FunctionType(
        code=method.__code__,
        globals=global_namespace,
        name=method.__name__,
        argdefs=method.__defaults__,
        closure=method.__closure__,
    )


@contextmanager
def _mutable_context(tree: PyTree, *, kopy: bool = False):
    tree = copy.copy(tree) if kopy else tree
    ovars(tree)[_MUTABLE] = True
    yield tree
    ovars(tree).pop(_MUTABLE, None)


def _setattr(self: PyTree, key: str, value: Any) -> None:
    if _MUTABLE not in ovars(self):
        # default behavior for frozen instances
        msg = f"Cannot set {key}={value!r}. Use `.at['{key}'].set({value!r})` instead."
        raise AttributeError(msg)

    if key in _field_registry[type(self)]:
        # apply the callbacks on setting the value
        # check if the key is a field name
        for callback in _field_registry[type(self)][key].callbacks:
            try:
                # callback is a function that takes the value of the field
                # and returns a modified value
                value = callback(value)
            except Exception as e:
                msg = f"Error for field=`{key}`:\n{e}"
                raise type(e)(msg)

    # set the value
    ovars(self)[key] = value  # type: ignore


def _delattr(self, key: str) -> None:
    # Delete the attribute if tree is not frozen
    if _MUTABLE not in ovars(self):
        raise AttributeError(f"Cannot delete {key}.")
    del ovars(self)[key]


def _init_wrapper(init_func: Callable) -> Callable:
    @ft.wraps(init_func)
    def wrapper(self, *a, **k) -> None:
        with _mutable_context(self):
            output = init_func(self, *a, **k)

            if post_init_func := getattr(type(self), _POST_INIT, None):
                # to simplify the logic, we call the post init method
                # even if the init method is not code-generated.
                post_init_func(self)

        # handle non-initialized fields
        if len(keys := set(_field_registry[type(self)]) - set(ovars(self))) > 0:
            msg = f"Uninitialized fields: ({', '.join(keys)}) "
            msg += f"in class `{type(self).__name__}`"
            raise AttributeError(msg)

        if wrapper.has_run is False:
            # handle instance variables of registered types once per class
            wrapper.has_run = True
            # auto registers the instance value if it is a registered `treeclass`
            # this behavior is similar to PyTorch behavior in `nn.Module`
            # with `Parameter` class. where registered classes are equivalent to nn.Parameter.
            # the behavior is useful to avoid repetitive code pattern in field definition and
            # and initialization inside init method.
            for key in ovars(self):
                if (
                    key not in _field_registry[type(self)]
                    and type(value := ovars(self)[key]) in _field_registry
                ):
                    # register the field with `init=False`.the field is not part of
                    # the init method signature, but defined in the `__post_init__` method
                    field = Field(name=key, type=type(value), init=False)
                    register_pytree_field_map(type(self), {key: field})
        return output

    wrapper.has_run = False
    return wrapper
