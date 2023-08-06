# aimlogpy

## Description

This is a Python Package to generate logs in a local file y the root of the app where is used.

## usage

```python
aimlogpy({})
aimlogpy([])
aimlogpy("Example")
```

## Installation

As simple as any package of Python, you just need to execute in your terminal the next command.

```bash
pip install aimlogpy
```

## Test´s with PYTEST

```log
=============================================================== test session starts ===============================================================
platform darwin -- Python 3.11.1, pytest-7.2.2, pluggy-1.0.0
rootdir: /Users/mianicoleruizgreco/Developer/p/python/aim-log-py
plugins: anyio-3.6.2
collected 5 items

main_test.py .....                                                                                                                          [100%]

================================================================ 5 passed in 0.02s ================================================================
```

### Results as example of the test´s.

```log
2023-04-07T23:23:59.950381 | [Type of Object]: bool           | [content]: True
2023-04-07T23:23:59.951181 | [Type of Object]: float          | [content]: 3.14
2023-04-07T23:23:59.951901 | [Type of Object]: complex        | [content]: (2+3j)
2023-04-07T23:23:59.952389 | [Type of Object]: CustomObject   | [content]: CustomObject
2023-04-07T23:23:59.952823 | [Type of Object]: str            | [content]:
```

## Contact: miarg49@gmail.com
