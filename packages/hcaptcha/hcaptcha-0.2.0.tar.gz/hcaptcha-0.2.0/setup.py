# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hcaptcha']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0', 'aiohttp>=3.8.4,<4.0.0']

setup_kwargs = {
    'name': 'hcaptcha',
    'version': '0.2.0',
    'description': 'A Python package for integrating hCaptcha, a popular captcha service, into various applications for enhanced security and user verification.',
    'long_description': '# hcaptcha\nhcaptcha is a Python module (unofficial) that provides an easy-to-use interface for verifying hcaptcha responses using the hcaptcha verification API.\n\n## Installation\nYou can install hcaptcha using pip:\n\n```bash\npip install hcaptcha\n```\n\n## Usage\nTo use hcaptcha, you\'ll need an hcaptcha secret key for your site. You can get one by signing up for an account at [hcaptcha website](https://hCaptcha.com/?r=cc7220f46013).\n\n```python\nfrom hcaptcha.hcaptcha import HCaptchaVerifier, HCaptchaVerificationError\n\n# Initialize the verifier with your hcaptcha secret key\nverifier = HCaptchaVerifier(your_hcaptcha_secret_key)\n\n# Verify an hcaptcha response\ntry:\n    is_valid = await verifier.verify(user_response_token)\n    if is_valid:\n        print("Captcha verified successfully.")\n    else:\n        print("Captcha verification failed.")\nexcept HCaptchaVerificationError as e:\n    print(f"Verification failed with error: {str(e)}")\n```\n## Documentation\nDocumentation for hcaptcha is available [here](https://github.com/VaibhavSys/hcaptcha/blob/master/docs/sources/api/hcaptcha.md)\n\n## Contributing\nIf you find a bug or have a feature request, please open an issue on [GitHub](https://github.com/VaibhavSys/hcaptcha).\n\n## Licence\nhcaptcha is distributed under the MIT License. See LICENSE for more information.',
    'author': 'Vaibhav Dhiman',
    'author_email': 'vaibhavsys@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VaibhavSys/hcaptcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
