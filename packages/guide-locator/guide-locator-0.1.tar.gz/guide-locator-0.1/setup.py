from setuptools import setup

setup(
    name='guide-locator',
    version='0.1',
    description='Library to get status guide of Unimed or Intermed',
    url='https://github.com/Simntek/Guide-Locator',
    author='Iran Alves',
    author_email='iranildo.alves10@hotmail.com',
    license='MIT',
    packages=['guide-locator'],
    install_requires=[
        'selenium',
        'webdriver-manager',
    ],
)
