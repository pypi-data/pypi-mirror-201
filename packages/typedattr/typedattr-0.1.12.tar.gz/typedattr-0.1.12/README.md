# typedattr

<p align="center">
<a href="https://github.com/gingsi/typedattr/actions/workflows/build_py37.yml">
  <img alt="build 3.7 status" title="build 3.7 status" src="https://img.shields.io/github/actions/workflow/status/gingsi/typedattr/build_py37.yml?branch=main&label=build%203.7" />
</a>
<a href="https://github.com/gingsi/typedattr/actions/workflows/build_py39.yml">
  <img alt="build 3.9 status" title="build 3.9 status" src="https://img.shields.io/github/actions/workflow/status/gingsi/typedattr/build_py39.yml?branch=main&label=build%203.9" />
</a>
<img alt="coverage" title="coverage" src="docs/coverage.svg" />
<a href="https://pypi.org/project/typedattr/">
  <img alt="version" title="version" src="https://img.shields.io/pypi/v/typedattr?color=success" />
</a>
</p>

Typechecking and conversion utility for [attrs](https://www.attrs.org/en/stable/)

Parses a dictionary into an attrs instance.
Contains other generic object, type and cache utilities.

## Install

Requires `python>=3.7`

```bash
pip install typedattr
```

## Quickstart

Define the class hierarchy and parse the input:

~~~python
from attrs import define
from typing import Optional
from typedattr import attrs_from_dict

@define
class Cfg:
    foo: int = 12
    bar: Optional[int] = None

print(attrs_from_dict(Cfg, {"foo": 1, "bar": 2}))
# Cfg(foo=1, bar=2)


@define
class CfgNested:
    sub_cfg: Cfg = None

print(attrs_from_dict(CfgNested, {"sub_cfg": {"foo": 1, "bar": 2}}))
# CfgNested(sub_cfg=Cfg(foo=1, bar=2))
~~~

## Features

* `@definenumpy` decorator for equality check if the instances contains numpy arrays
* Nested checking and conversion of python standard types
* Supports old and new style typing (e.g. `typing.List` and `list`)
* Supports positional and keyword arguments in classes
* Can also typecheck existing attrs instances
* Allows custom conversions, by default converts source type `str` to target type `Path` and
  `int` to `float`
* Allows to redefine which objects will be recursed into, by default recurses into standard
  containers (list, dict, etc.)

### Strict mode (default)

* Convert everything to the target type, e.g. if the input is a list and the annotation is a tuple,
  the output will be a tuple
* Raise errors if types cannot be matched, there are unknown fields in the input or
  abstract annotation types are used (e.g. Sequence)

### Non-strict mode

Enabled by calling `attrs_from_dict` with `strict=False`

* No conversion except for creating the attrs instance from the dict
* Ignore silently if types cannot be matched or abstract annotation types are used
* Unknown fields in the input will be added to the attrs instance if possible
  (see the hint below about slots)

### Skip unknowns

Set `skip_unknowns=True` to ignore all unknown input fields.

### Hints

The following behaviour stems from the `attrs` package:

* New attributes cannot to be added after class definition to an attrs instance,
  unless it is created with `@define(slots=False)`
  [Explanation](https://www.attrs.org/en/21.2.0/glossary.html#term-slotted-classes)
* Untyped fields or "ClassVar" typed fields will be ignored by @attrs.define
  and therefore also by this library.

### Possible improvements

* Supports Callable but does not typecheck the signature
* Not tested for NewType, Literal

## Install locally and run tests

Clone repository and cd into, then:

~~~bash
pip install -e .
pip install pytest pytest-cov pylint
pylint typedattr

# run tests for python>=3.7
python -m pytest --cov
pylint tests

# run tests for python>=3.9
python -m pytest tests_py39 --cov
pylint tests_py39
~~~

## Alternatives

This library should be useful for off-the-shelf typechecking and conversion of dicts to
attrs instances.

For more complex or other related use cases there are many alternatives:
`cattrs`, `attrs-strict`, `pydantic`, `dataconf` to name a few.
