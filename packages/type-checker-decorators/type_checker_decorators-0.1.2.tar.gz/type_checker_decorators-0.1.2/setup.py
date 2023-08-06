# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_checker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'type-checker-decorators',
    'version': '0.1.2',
    'description': '',
    'long_description': '# How to Import\n```\nfrom type_checker.decorators import enforce_strict_types\n```\n\n\n# Examples utilisation\n```\nfrom dataclasses import dataclass\n\nfrom type_checker.decorators import enforce_strict_types\n\n\n@enforce_strict_types\n@dataclass\nclass Person:\n    name: str\n    age: int\n\n\ndef test_greet_person_with_wrong_types():\n    try:\n        Person(123, "twenty")\n    except TypeError as e:\n        assert (\n            str(e)\n            == "Problem on function Person, Expected type \'<class \'str\'>\' for argument \'name\' but received type \'<class \'int\'>\' instead"\n        )\n    try:\n        Person("Alice", "twenty")\n    except TypeError as e:\n        assert (\n            str(e)\n            == "Problem on function Person, Expected type \'<class \'int\'>\' for argument \'age\' but received type \'<class \'str\'>\' instead"\n        )\n\n```\n\n\n```\nfrom type_checker.decorators import enforce_strict_types\n\n\n@enforce_strict_types\ndef greet(name: str, age: int):\n    print(f"Hello, {name}! You are {age} years old.")\n\n\ndef test_greet_with_wrong_types():\n    try:\n        greet(123, "twenty")\n    except TypeError as e:\n        print(str(e))\n        assert (\n            str(e)\n            == "Problem on function greet, Expected type \'<class \'str\'>\' for argument \'name\' but received type \'<class \'int\'>\' instead"\n        )\n    try:\n        greet("Alice", "twenty")\n    except TypeError as e:\n        assert (\n            str(e)\n            == "Problem on function greet, Expected type \'<class \'int\'>\' for argument \'age\' but received type \'<class \'str\'>\' instead"\n        )\n\n```',
    'author': 'Aboussejra',
    'author_email': 'Amir.Boussejra@viavisolutions.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
