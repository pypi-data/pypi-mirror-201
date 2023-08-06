# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_common',
 'pytorch_common.callbacks',
 'pytorch_common.callbacks.mixin',
 'pytorch_common.callbacks.output',
 'pytorch_common.callbacks.output.plot',
 'pytorch_common.error',
 'pytorch_common.kfoldcv',
 'pytorch_common.kfoldcv.strategy',
 'pytorch_common.modules',
 'pytorch_common.util']

package_data = \
{'': ['*']}

install_requires = \
['bunch>=1.0.1',
 'ipython>=7.31.0',
 'matplotlib>=3.5.1',
 'numpy>=1.20',
 'scikit-learn>=1.0.2',
 'seaborn>=0.11.2',
 'torch>=1.10.1']

setup_kwargs = {
    'name': 'pytorch-common',
    'version': '0.1.0',
    'description': 'Common torch tools and extension',
    'long_description': "# pytorch-common\n\nA [Pypi module](https://pypi.org/project/pytorch-common/) with pytorch common tools like:\n\n\n## Build release\n\n**Step 1**: Increase version into next files:\n\n```bash\npytorch_common/__init__.py\npyproject.toml\n```\n\n**Step 2**: Build release.\n\n```bash\n$ poetry build                                                                                                                                                                                                                 \ue0b2 ✔ \ue0b3 \n\nBuilding pytorch-common (0.0.22)\n  - Building sdist\n  - Built pytorch-common-0.0.22.tar.gz\n  - Building wheel\n  - Built pytorch_common-0.0.22-py3-none-any.whl\n```\n\n**Step 3**: Publish release to PyPI repository.\n\n```bash\n$ poetry build                                                                                                                                                                                                                 \ue0b2 ✔ \ue0b3 \n\nUsername: user_name\nPassword: a pass\n\nPublishing pytorch-common (0.0.22) to PyPI\n - Uploading pytorch-common-0.0.22.tar.gz 100%\n - Uploading pytorch_common-0.0.22-py3-none-any.whl 100%\n```\n\n\n## Features\n\n* **Callbacks** (keras style)\n  * **Validation**: Model validation.\n  * **ReduceLROnPlateau**:\n    * Reduce learning rate when a metric has stopped improving.\n    * Models often benefit from reducing the learning rate by a factor\n      of 2-10 once learning stagnates. This scheduler reads a metrics\n      quantity and if no improvement is seen for a 'patience' number\n      of epochs, the learning rate is reduced.\n  * **EarlyStop**:\n    * Stop training when model has stopped improving a specified metric.\n  * **SaveBestModel**:\n    * Save model weights to file while model validation metric improve.\n  * **Logger**:\n    * Logs context properties.\n    * In general is used to log performance metrics every n epochs.\n  * **MetricsPlotter**:\n    * Plot evaluation metrics.\n    * This graph is updated every n epochs during training process.\n  * **Callback** and **OutputCallback**:\n    * Base classes.\n  * **CallbackManager**:\n    * Simplify callbacks support to fit custom models.\n* **StratifiedKFoldCV**:\n  * Support parallel fold processing on CPU.\n* **Mixins**\n  * FiMixin\n  * CommonMixin\n  * PredictMixin\n  * PersistentMixin\n* **Utils**\n  * device management\n  * stopwatch\n  * data split\n  * os\n  * model\n  * LoggerBuilder\n\n## Examples\n\n### Device management\n\n\n```python\nimport pytorch_common.util as pu\n\n# Setup prefered device.\npu.set_device_name('gpu') # / 'cpu'\n\n# Setup GPU memory fraction for a process (%).\npu.set_device_memory(\n  'gpu' # / 'cpu',\n  process_memory_fraction=0.5\n)\n\n# Get prefered device.\n# Note: In case the preferred device is not found, it returns CPU as fallback.\ndevice = pu.get_device()\n```\n\n### Logging\n\n\n```python\nimport logging\nimport pytorch_common.util as pu\n\n## Default loggin in console...\npu.LoggerBuilder() \\\n .on_console() \\\n .build()\n\n## Setup format and level...\npu.LoggerBuilder() \\\n .level(logging.ERROR) \\\n .on_console('%(asctime)s - %(levelname)s - %(message)s') \\\n .build()\n```\n\n\n### Stopwatch\n\n\n```python\nimport logging\nimport pytorch_common.util as pu\n\nsw = pu.Stopwatch()\n\n# Call any demanding process...\n\n# Get resposne time.\nresposne_time = sw.elapsed_time()\n\n# Log resposne time.\nlogging.info(sw.to_str())\n```\n\n\n### Dataset split\n\n\n```python\nimport pytorch_common.util as pu\n\ndataset = ... # <-- Torch.utils.data.Dataset\n\ntrain_subset, test_subset = pu.train_val_split(\n  dataset,\n  train_percent = .7\n)\n\ntrain_subset, val_subset, test_subset = pu.train_val_test_split(\n  dataset,\n  train_percent = .7,\n  val_percent   = .15\n)\n```\n\n\n### Kfolding\n\n```python\nimport logging\nfrom pytorch_common.kfoldcv import StratifiedKFoldCV, \\\n                                   ParallelKFoldCVStrategy, \\\n                                   NonParallelKFoldCVStrategy\n\n# Call your model under this function..\ndef train_fold_fn(dataset, train_idx, val_idx, params, fold):\n  pass\n\n# Get dataset labels\ndef get_y_values_fn(dataset):\n  pass\n\ncv = StratifiedKFoldCV(\n  train_fold_fn,\n  get_y_values_fn,\n  strategy=NonParallelKFoldCVStrategy() # or ParallelKFoldCVStrategy()\n  k_fold = 5\n)\n\n# Model hyperparams...\nparams = {\n    'seed': 42,\n    'lr': 0.01,\n    'epochs': 50,\n    'batch_size': 4000,\n    ...\n}\n\n# Train model...\nresult = cv.train(dataset, params)\n\nlogging.info('CV results: {}'.format(result))\n```\n\n\n### Assertions\n\n\n```python\nfrom pytorch_common.error import Assertions, Checker\n\n# Check functions and construtor params usign assertions..\n\nparam_value = -1\n\n# Raise an exception with 404103 eror code when the condition is not met \nAssertions.positive_int(404103, param_value, 'param name')\n\nAssertions.positive_float(404103, param_value, 'param name')\n\n# Other options\nAssertions.is_class(404205, param_value, 'param name', aClass)\n\nAssertions.is_tensor(404401, param_value, 'param name')\n\nAssertions.has_shape(404401, param_value, (3, 4), 'param name')\n\n# Assertions was impelemented using a Checker builder:\n\n Checker(error_code, value, name) \\\n    .is_not_none() \\\n    .is_int() \\\n    .is_positive() \\\n    .check()\n\n# Other checker options..\n#   .is_not_none()\n#   .is_int()\n#   .is_float()\n#   .is_positive()\n#   .is_a(aclass)\n#   .is_tensor()\n#   .has_shape(shape)\n```\n\n\n### Callbacks\n\n```python\nfrom pytorch_common.callbacks import CallbackManager\n\nfrom pytorch_common.callbacks import EarlyStop, \\\n                                     ReduceLROnPlateau, \\\n                                     Validation\n\nfrom pytorch_common.callbacks.output import Logger, \\\n                                            MetricsPlotter\n\n\ndef train_method(model, epochs, optimizer, loss_fn, callbacks):\n\n callback_manager = CallbackManager(epochs, optimizer, loss_fn, model, callbacks)\n\n for epoch in range(epochs):\n            callback_manager.on_epoch_start(epoch)\n\n            # train model...\n\n            callback_manager.on_epoch_end(train_loss)\n\n            if callback_manager.break_training():\n                break\n\n  return callback_manager.ctx\n\n\nmodel     = # Create my model...\noptimizer = # My optimizer...\nloss_fn   = # my lost function\n\ncallbacks = [\n   # Log context variables after each epoch...\n   Logger(['fold', 'time', 'epoch', 'lr', 'train_loss', 'val_loss', ... ]),\n\n   EarlyStop(metric='val_auc', mode='max', patience=3),\n   \n   ReduceLROnPlateau(metric='val_auc'),\n  \n   Validation(\n       val_set,\n       metrics = {\n           'my_metric_name': lambda y_pred, y_true: # calculate validation metic,\n           ...\n       },\n       each_n_epochs=5\n   ),\n   \n   SaveBestModel(metric='val_loss'),\n   \n   MetricsPlotter(metrics=['train_loss', 'val_loss'])\n]\n\n\ntrain_method(model, epochs=100, optimizer, loss_fn, callbacks)\n```\n\nGo to next projects to see funcional code examples:\n\n- https://github.com/adrianmarino/deep-fm\n- https://github.com/adrianmarino/attention\n\n\n",
    'author': 'adrianmarino',
    'author_email': 'adrianmarino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adrianmarino/pytorch-common/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
