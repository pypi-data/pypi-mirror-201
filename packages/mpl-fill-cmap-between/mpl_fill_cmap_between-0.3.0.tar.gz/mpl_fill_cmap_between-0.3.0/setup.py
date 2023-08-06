# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mpl_fill_cmap_between']
install_requires = \
['matplotlib>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'mpl-fill-cmap-between',
    'version': '0.3.0',
    'description': 'Create fillbetween plots filled with any colormap',
    'long_description': '# mpl_fill_cmap_between\n\nCreate fill_between-like plots filled with any matplotlib\'s colormap.\n\n## Install\n\n```bash\npip install mpl_fill_cmap_between\n```\n\n\n## Examples\n\nThe function `fill_cmap_between` (and also the function `fill_cmap_between_x`) can be used in the following manner:\n\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom mpl_fill_cmap_between import fill_cmap_between, fill_cmap_between_x\n\nx = np.linspace(-10, 10, 50)\ny = x**2 - 40\n\nfig = plt.figure(figsize=(4.8, 2.0))\nax = fig.add_subplot(111)\n\nfill_cmap_between(x, y * 0.1, 0, ax=ax, cmap="viridis", kw_line_1=dict(color="k"),\n                  kw_line_2=dict(color="k", lw=0.5))\nax.set_aspect("equal")\n\nfig.tight_layout()\nfig.savefig("example.pdf", dpi=300)\n```\n\n![Example](examples/example.png)\n\n\nThe plot can also be rotated by an angle from a given origin:\n\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom mpl_fill_cmap_between import fill_cmap_between, fill_cmap_between_x\n\nx = np.linspace(0, 10, 50)\ny = (x - 5)**2 - 10\n\nfig = plt.figure(figsize=(4.8, 2.0))\nax = fig.add_subplot(111)\n\nfill_cmap_between(x, y * 0.1, 0, ax=ax, cmap="viridis", kw_line_1=dict(color="k"),\n                  kw_line_2=dict(color="k", lw=0.5), angle=40, origin=(10, 0))\nax.set_aspect("equal")\nax.grid(True, ls=":")\n\nfig.tight_layout()\nfig.savefig("example_02.png", dpi=300)\n```\n\n![Example](examples/example_02.png)\n',
    'author': 'Cristóbal Tapia Camú',
    'author_email': 'crtapia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cristobaltapia/mpl_fill_cmap_between',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
