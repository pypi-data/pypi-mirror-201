# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embeddings',
 'embeddings.config',
 'embeddings.data',
 'embeddings.embedding',
 'embeddings.evaluator',
 'embeddings.metric',
 'embeddings.model',
 'embeddings.model.lightning_module',
 'embeddings.pipeline',
 'embeddings.task',
 'embeddings.task.lightning_task',
 'embeddings.task.sklearn_task',
 'embeddings.transformation',
 'embeddings.transformation.hf_transformation',
 'embeddings.transformation.pandas_transformation',
 'embeddings.utils',
 'embeddings.utils.lightning_callbacks',
 'experimental',
 'experimental.datasets',
 'experimental.datasets.utils',
 'experimental.embeddings',
 'experimental.embeddings.language_models']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0',
 'appdirs>=1.4.4',
 'click==8.0.4',
 'datasets>=1.16.1',
 'evaluate>=0.4.0',
 'numpy>=1.20.0,<=1.23.4',
 'optuna>=2.9.1',
 'pydantic>=1.8.2',
 'pytorch-lightning==1.5.4',
 'requests>=2.25.1',
 'sacremoses>=0.0.53',
 'scikit-learn>=1.0.0',
 'scipy>=1.6.2',
 'seqeval>=1.2.2',
 'setuptools>=65.5.1',
 'srsly>=2.4.1',
 'tensorboard>=2.4.1',
 'tokenizers>=0.13.2',
 'torch>=1.9,<1.12.0',
 'transformers>=4.26.0',
 'typer>=0.4.0',
 'types-PyYAML>=5.4.10',
 'types-setuptools>=57.4.11',
 'wandb>=0.12.10']

extras_require = \
{':extra == "developer"': ['typing-extensions>=4.0.1.0'],
 ':sys_platform == "win32"': ['intel-openmp>=2022.0.3,<2023.0.0']}

setup_kwargs = {
    'name': 'clarinpl-embeddings',
    'version': '0.0.1rc4606821465119',
    'description': '',
    'long_description': 'None',
    'author': 'Roman Bartusiak',
    'author_email': 'riomus@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CLARIN-PL/embeddings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
