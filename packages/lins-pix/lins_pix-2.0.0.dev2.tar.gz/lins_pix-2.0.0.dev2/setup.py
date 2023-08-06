# python3 setup.py sdist upload -r testpypi
# pip install -i https://test.pypi.org/simple/ lins_pix==0.0.14

from distutils.core import setup
from setuptools import find_packages
from lins_pix import __version__


setup(
    name='lins_pix',
    description='Pacote para gerenciar transacoes PIX',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'qrcode==7.3.1',
        'requests==2.27.1',
        'PyJWT==1.7.1',
        'lins-log==2.1.4.33',
        'graypy==1.1.2'
    ],
    url='https://bitbucket.org/grupolinsferrao/pypck-lins-pix/',
    author='Gustavo Schaedler',
    author_email='gustavopoa@gmail.com',
    license='MIT',
)
