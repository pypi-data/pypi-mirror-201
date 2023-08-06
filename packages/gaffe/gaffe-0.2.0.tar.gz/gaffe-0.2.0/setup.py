# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaffe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gaffe',
    'version': '0.2.0',
    'description': 'Simple structured exceptions for python.',
    'long_description': '# Introducing Gaffe: Streamlined Exception Handling for Python\n\nAre you tired of managing messy, unstructured exceptions in your Python projects? Gaffe is here to save the day! This elegant library offers a metaclass-based approach for highly extensible and easy-to-integrate custom exceptions, leading to better error handling and improved code readability.\n\n## 🔥 Key Features\n\n- 🎯 Simple, concise syntax for defining custom errors with optional subtypes\n- 🧩 Clean integration through metaclass-based approach\n- 🌳 Supports inheritance and composition of custom errors\n- 🏗️ Automatic generation of error classes with custom attributes\n- 🧮 Easy error comparison with the __eq__ method, supporting both class and instance comparisons\n- 🕵️\u200d♂️ raises decorator to inspect and validate exceptions raised by functions or methods\n- 🚀 Quick Installation\n\nFor pip enthusiasts:\n\n```bash\npip install gaffe\n```\n\nFor poetry aficionados:\n\n```bash\npoetry add gaffe\n```\n\n# 💡 Getting Started\n\nTo employ Gaffe\'s custom error system, import the Error class and create custom errors by inheriting from it:\n\n```python\nfrom gaffe import Error\n\nclass NotFoundError(Exception):\n    ...\n\nclass MyError(Error):\n    not_found: NotFoundError\n    invalid_input: ...\n    authentication_error = "authentication_error"\n```\n    \nWith this example, you\'ll get three custom errors under the MyError class, ready to be used just like any other Python exceptions.\n\n## 🎩 Raises Decorator\n\nHarness the power of the raises decorator to define and validate the types of exceptions a function or method can raise:\n\n```python\nfrom gaffe import raises\n\n@raises(TypeError, ValueError)\ndef my_function(x: int, y: int) -> float:\n    if x <= 0 or y <= 0:\n        raise ValueError("x and y must be positive")\n    return x / y\n```\n\nThe raises decorator ensures that my_function can only raise TypeError and ValueError. If it tries to raise an unlisted exception, an AssertionError will be raised with a suitable error message.\n\n## 🤖 Mypy Integration\n\nTo keep mypy happy, use the gaffe.mypy:plugin in your config file, and ensure that error properties are annotated with `Exception` type instead of `...`\n\n```toml\n[tool.mypy]\nplugins = "gaffe.mypy:plugin"\n```\n\n\nReady to revolutionize your Python exception handling? Get started with Gaffe today and check out the test scenarios for more examples!\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kodemore/gaffe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
