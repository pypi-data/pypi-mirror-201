# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onestep', 'onestep.broker', 'onestep.middleware', 'onestep.store']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.6.0,<4.0.0', 'blinker>=1.5,<2.0', 'croniter>=1.3.8,<2.0.0']

extras_require = \
{'rabbitmq': ['amqpstorm>=2.10.6,<3.0.0']}

setup_kwargs = {
    'name': 'onestep',
    'version': '0.1.7',
    'description': '',
    'long_description': '# OneStep\n\n<a href="https://github.com/mic1on/onestep/actions/workflows/test.yml?query=event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/mic1on/onestep/workflows/test%20suite/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://pypi.org/project/onestep" target="_blank">\n    <img src="https://img.shields.io/pypi/v/onestep.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/onestep" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/onestep.svg" alt="Supported Python versions">\n</a>\n\n<hr />\n仅需一步，轻松实现分布式异步任务。\n\n## Brokers\n\n- [x] MemoryBroker\n- [x] CronBroker\n- [x] WebHookBroker\n- [x] RabbitMQBroker\n- [ ] RedisBroker\n- [ ] KafkaBroker\n\n## example\n\n```python\nfrom onestep import step, WebHookBroker\n\n\n# 对外提供一个webhook接口，接收外部的消息\n@step(from_broker=WebHookBroker(path="/push"))\ndef waiting_messages(message):\n    print("收到消息：", message)\n\n\nif __name__ == \'__main__\':\n    step.start(block=True)\n```\n\n```python\nfrom onestep import step, CronBroker\n\n\n# 每3秒触发一次任务\n@step(from_broker=CronBroker("* * * * * */3", a=1))\ndef cron_task(message):\n    assert message.body == {"a": 1}\n    return message\n\n\nif __name__ == \'__main__\':\n    step.start(block=True)\n```\n\n更多例子请参阅：[examples](example)',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
