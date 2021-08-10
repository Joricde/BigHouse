import os

import setuptools


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires


setuptools.setup(
    name='BigHouse',
    version='1.0',
    packages=setuptools.find_packages(),
    install_requires=_process_requirements()
)
