# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_typed', 'flask_typed.docs']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16',
 'flask>=2.2.3,<3.0.0',
 'openapi-schema-pydantic>=1.2.4,<2.0.0',
 'pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'flask-typed',
    'version': '0.1.2rc1',
    'description': '',
    'long_description': '# flask-typed\n\nA Flask extension for developing HTTP APIs using type annotations. Type annotations are used for the validation of requests and generating API documentation.\n\n## Example\n\n```python\nfrom flask import Flask\nfrom pydantic import BaseModel\n\nfrom flask_typed import TypedResource, TypedAPI\n\n\nclass HelloResponse(BaseModel):\n\n    message: str\n    sender: str\n    receiver: str\n\n\nclass HelloResource(TypedResource):\n\n    def get(self, sender: str, receiver: str) -> HelloResponse:\n        """\n        Greets someone\n\n        :param sender: Greeter\n        :param receiver: The one being greeted\n        :return: Greetings\n        """\n        return HelloResponse(\n            message=f"Hello to {receiver} from {sender}!",\n            sender=sender,\n            receiver=receiver\n        )\n\n\napp = Flask(__name__)\napi = TypedAPI(app, version="1.0", description="Greetings API")\n\napi.add_resource(HelloResource, "/hello/<sender>")\n\nif __name__ == "__main__":\n    app.run()\n```',
    'author': 'Mustafa Efendioğlu',
    'author_email': 'mfnd@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
