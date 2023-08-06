# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ask_robot']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.3,<3.0.0',
 'bs4>=0.0.1,<0.0.2',
 'cryptography>=39.0.2,<40.0.0',
 'openai>=0.27.2,<0.28.0',
 'requests>=2.28.2,<3.0.0',
 'wechatpy>=1.8.18,<2.0.0']

entry_points = \
{'console_scripts': ['ask = ask_robot.main:main']}

setup_kwargs = {
    'name': 'ask-robot',
    'version': '0.0.4',
    'description': 'the robot for chat system',
    'long_description': "\n# Ask robot\n\n**for WeChat platform, offer api to do an ask robot.**\n\n\n\n\n\n# install python from source\n\n```shell\nwget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz\ntar -xzvf Python-3.9.7.tar.xz\n\ncd Python-3.9.7\n./configure --prefix=/opt/idlepig/apps/python397\nmake\nmake altinstall\n\ncd ~/code/venv\n/opt/idlepig/apps/python397/bin/python3.9 -m venv wx\nsource ~/code/venv/wx/bin/activate\n\ncd ~/code/wx\npip install -r requirements.txt\n```\n\n\n# or install python directly\n\n\nin centos\n\n```shell\nyum install python36u\n```\n\n# env\n\ncreate virtual environment and source\n\n```shell\nmkdir -p ~/code/venv\ncd ~/code/venv\npython3 -m venv wx\nsource ~/code/venv/wx/bin/activate\n```\n\n\n\n# install ask_robot\n\n```\npip install ask_robot\n```\n\n\n\n# start flask service\n\nyou need set actual info for token, aes_key, appid\n\nif you are in plaintext mode, just set token is ok.\n\n```shell\nexport token=''\nexport app_id=''\nexport aes_key=''\nexport secret=''\nexport email_from=''\nexport email_password=''\nexport email_to=''\nexport chatgpt=''\n```\n\n```\nnohup ask &\n```\n\nthen http://0.0.0.0:8081 will work\n\n\n# install nginx\n\n\n```shell\nyum install nginx\n```\n\nvi /etc/nginx/nginx.conf\n\n```shell\nhttp {\n...\nupstream idlewith {\n    server 127.0.0.1:8081;\n  }\n...\n}\n```\n\nvi /etc/nginx/conf.d/default.conf\n\n```shell\nserver {\n    listen 80;\n    server_name _;\n    location / {\n      proxy_pass http://idlewith;\n    }\n}\n```\n\nso, we map 80 port to 8081 port\n\nstart nginx\n\n```shell\nnginx\n```\n",
    'author': 'idlewith',
    'author_email': 'newellzhou@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
