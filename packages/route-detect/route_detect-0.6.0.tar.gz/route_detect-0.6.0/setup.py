# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routes', 'routes.commands', 'routes.rules', 'routes.templates']

package_data = \
{'': ['*']}

install_requires = \
['semgrep>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['routes = routes.main:main']}

setup_kwargs = {
    'name': 'route-detect',
    'version': '0.6.0',
    'description': 'Find web application HTTP route authn and authz security bugs in your code.',
    'long_description': '# route-detect\n\n[![CI](https://github.com/mschwager/route-detect/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mschwager/route-detect/actions/workflows/ci.yml)\n[![Python Versions](https://img.shields.io/pypi/pyversions/route-detect.svg)](https://pypi.org/project/route-detect/)\n[![PyPI Version](https://img.shields.io/pypi/v/route-detect.svg)](https://pypi.org/project/route-detect/)\n\nFind authentication (authn) and authorization (authz) security bugs in web application routes.\n\nWeb application HTTP route authn and authz bugs are some of the most common security issues found today. These industry standard resources highlight the severity of the issue:\n\n- 2021 OWASP Top 10 #1 - [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)\n- 2021 OWASP Top 10 #7 - [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) (formerly Broken Authentication)\n- 2019 OWASP API Top 10 #2 - [Broken User Authentication](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa2-broken-user-authentication.md)\n- 2019 OWASP API Top 10 #5 - [Broken Function Level Authorization](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa5-broken-function-level-authorization.md)\n- 2022 CWE Top 25 #14 - [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/1387.html)\n- 2022 CWE Top 25 #16 - [CWE-862: Missing Authorization](https://cwe.mitre.org/data/definitions/1387.html)\n- 2022 CWE Top 25 #18 - [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/1387.html)\n- #21 most CVEs by CWE - [CWE-284: Access Control (Authorization) Issues](https://www.cvedetails.com/cwe-definitions.php)\n- #47 most CVEs by CWE - [CWE-639: Access Control Bypass Through User-Controlled Key](https://www.cvedetails.com/cwe-definitions.php)\n\n![Routes demo](routes-demo.png?raw=true)\n\n<p align="center">\n    <i>Routes from <code><a href="https://github.com/koel/koel">koel<a></code> streaming server</i>\n</p>\n\nSupported web frameworks (`route-detect` IDs in parentheses):\n\n- Python: Django (`django`, `django-rest-framework`), Flask (`flask`), Sanic (`sanic`)\n- PHP: Laravel (`laravel`), Symfony (`symfony`), CakePHP (`cakephp`)\n- Ruby: Rails (`rails`), Grape (`grape`)\n- Java: JAX-RS (`jax-rs`), Spring (`spring`)\n- Go: Gorilla (`gorilla`), Gin (`gin`), Chi (`chi`)\n- JavaScript/TypeScript: Express (`express`), React (`react`), Angular (`angular`)\n\n# Installing\n\nUse `pip` to install `route-detect`:\n\n```\n$ python -m pip install --upgrade route-detect\n```\n\nYou can check that `route-detect` is installed correctly with the following command:\n\n```\n$ echo \'print(1 == 1)\' | semgrep --config $(routes which test-route-detect) -\nScanning 1 file.\n\nFindings:\n\n  /tmp/stdin\n     routes.rules.test-route-detect\n        Found \'1 == 1\', your route-detect installation is working correctly\n\n          1┆ print(1 == 1)\n\n\nRan 1 rule on 1 file: 1 finding.\n```\n\n# Using\n\n`route-detect` provides the `routes` CLI command and uses [`semgrep`](https://github.com/returntocorp/semgrep) to search for routes.\n\nUse the `which` subcommand to point `semgrep` at the correct web application rules:\n\n```\n$ semgrep --config $(routes which django) path/to/django/code\n```\n\nUse the `viz` subcommand to visualize route information in your browser:\n\n```\n$ semgrep --json --config $(routes which django) --output routes.json path/to/django/code\n$ routes viz --browser routes.json\n```\n\nIf you\'re not sure which framework to look for, you can use the special `all` ID to check everything:\n\n```\n$ semgrep --json --config $(routes which all) --output routes.json path/to/code\n```\n\nIf you have custom authn or authz logic, you can copy `route-detect`\'s rules:\n\n```\n$ cp $(routes which django) my-django.yml\n```\n\nThen you can modify the rule as necessary and run it like above:\n\n```\n$ semgrep --json --config my-django.yml --output routes.json path/to/django/code\n$ routes viz --browser routes.json\n```\n\n# Contributing\n\n`route-detect` uses [`poetry`](https://python-poetry.org/) for dependency and configuration management.\n\nBefore proceeding, install project dependencies with the following command:\n\n```\n$ poetry install --with dev\n```\n\n## Linting\n\nLint all project files with the following command:\n\n```\n$ poetry run pre-commit run --all-files\n```\n\n## Testing\n\nRun Python tests with the following command:\n\n```\n$ poetry run pytest --cov\n```\n\nRun Semgrep rule tests with the following command:\n\n```\n$ poetry run semgrep --test --config routes/rules/ tests/test_rules/\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mschwager/route-detect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
