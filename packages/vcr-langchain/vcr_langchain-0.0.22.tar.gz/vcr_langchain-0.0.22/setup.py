# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcr_langchain']

package_data = \
{'': ['*']}

install_requires = \
['gorilla>=0.4.0,<0.5.0', 'langchain>=0.0.130,<0.0.131', 'vcrpy>=4.2.1,<5.0.0']

setup_kwargs = {
    'name': 'vcr-langchain',
    'version': '0.0.22',
    'description': 'Record and replay LLM interactions for langchain',
    'long_description': '# VCR LangChain\n\nPatches [VCR.py](https://github.com/kevin1024/vcrpy) to include non-network tooling for use with [LangChain](https://github.com/hwchase17/langchain). Refactor with confidence as you record and replay all your LLM logic in a contained environment, free from any and all side effects.\n\n## Quickstart\n\n```bash\npip install vcr-langchain\n```\n\nUse it with pytest:\n\n```python\nimport vcr_langchain as vcr\nfrom langchain.llms import OpenAI\n\n@vcr.use_cassette()\ndef test_use_as_test_decorator():\n    llm = OpenAI(model_name="text-ada-001")\n    assert llm("Tell me a surreal joke") == "<put the output here>"\n```\n\nThe next time you run it:\n\n- the output is now deterministic\n- it executes a lot faster by replaying from cache\n- no command executions or other side effects actually happen\n- you no longer need to have real API keys defined for test execution in CI environments\n\nFor more examples, see [the usages test file](tests/test_usage.py).\n\n### Pitfalls\n\nNote that tools, if initialized outside of the `vcr_langchain` decorator, will not have recording capabilities patched in. This is true even if an agent using those tools is initialized within the decorator.\n\n## Documentation\n\nFor more information on how VCR works and what other options there are, please see the [VCR docs](https://vcrpy.readthedocs.io/en/latest/index.html).\n\nFor more information on how to use langchain, please see the [langchain docs](https://langchain.readthedocs.io/en/latest/).\n\n**Please note that there is a lot of langchain functionality that I haven\'t gotten around to hijacking for recording.** If there\'s anything you need to record in a cassette, please open a PR or issue.\n\n## Projects that use this\n\n- [LangChain Visualizer](https://github.com/amosjyng/langchain-visualizer)\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
