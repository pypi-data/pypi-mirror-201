from setuptools import setup, find_packages

setup(
    name='magento_openedx_oauth',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'social-auth-core>=4.0,<5.0',
        'requests>=2.25,<3.0'
    ],
    author='Francisco Huerta Yumha',
    description='A Python package for Magento OAuth2 authentication',
    url='https://github.com/Francisco-Huerta/magento_openedx_oauth',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

