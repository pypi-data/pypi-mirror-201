from setuptools import setup, find_packages

setup(
    name='magento_oauth',
    version='0.2.3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'social-auth-core>=4.0,<5.0',
        'requests>=2.25,<3.0'
    ],
    author='Francisco Huerta Yumha',
    description='A Python package for Magento OAuth2 authentication',
    url='https://github.com/Francisco-Huerta/oauth_magento_openedx',
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