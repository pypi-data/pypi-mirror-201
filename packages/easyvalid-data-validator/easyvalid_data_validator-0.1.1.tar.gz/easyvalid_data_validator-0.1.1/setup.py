# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyvalid_data_validator',
 'easyvalid_data_validator.customexceptions',
 'easyvalid_data_validator.datacheckers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easyvalid-data-validator',
    'version': '0.1.1',
    'description': '',
    'long_description': '## Installation\n\nYou can install it directly from PyPi\n```bash\n  pip install easyvalid-data-validator\n```\n    \n## Tests\n\nAll functions are fully tested\n\nYou are able to run tests on your own by using this command being in package directory\n\n```bash\n  poetry run python -m unittest discover -v\n```\nor\n```bash\n  poetry run pytest\n```\n# easyvalid-data-validator\n\nIt\'s a package developed mainly for validation of json dict that is created by using json.load().\n\nHere is an example of json dict, that has name, age, and balance.\n```\nuser = {\n    "name": "ADAM",\n    "age": 18,\n    "balance": "2000.00"\n}\n```\nWe want to validate if:\n- name contain only uppercase letters,\n- age is greater or equal to 18,\n- balance is valid for Decimal conversion\n\n\nWe need to prepare constraint dict which describes this rules as explained:\n\n```\nconstraints = {\n    "key_name1": {<ConstraintEnumObject>: *args},\n    "key_name2": {<ConstraintEnumObject>: *args},\n    "key_name3": {<ConstraintEnumObject>: *args}\n}\n```\n\nSo we create dict that stores dicts containing Constraint Objects as key that are indicators for validator of which case it\'s currently working on, and what datachecker it should use.\nValue should be arguments that datachecker need:\n- Constraint Object - Enum object\n- datachecker - function that takes needed arguments and returns True or False if condition is mached\n- validator - validator function that raises error when any of value is not valid, or returns data when it\'s valid\n```\nfrom easyvalid_data_validator.constraints import Constraint\n\nconstraints = {\n    "name": {Constraint.STRING_REGEX: r\'^[A-Z]+$\'},\n    "age": {Constraint.INT_GE: 18},\n    "balance": {Constraint.STRING_IS_DECIMAL: None}\n}\n```\n\nValidation is very easy now, we just need to provide validate_json_data() with json_data, and constraints:\n\n```\nfrom easyvalid_data_validator.validator import validate_json_data\n\nresult = validate_json_data(user, constraints)\n\n# result --> {"name": "ADAM", "age": 18, "balance": "2000.00"}\n```\n\nIf we would change age of user to 17, validator would throw an error:\n\n```\nValidationError("age": ["Invalid integer expression - isn\'t grater or equal to compare value"])\n```\n\n## Documentation link\n\n[Click to read documentation](https://github.com/DSmolke/EASYVALID_DATA_VALIDATOR/edit/master/README.md)\n',
    'author': 'Smolke',
    'author_email': 'd.smolczynski1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
