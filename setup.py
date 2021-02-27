from setuptools import setup

README = open('README.md', 'r').read()
VERSION = '0.1.0'

setup(
    name = 'django-webpack-bridge',
    packages = ['webpack_bridge', 'webpack_bridge/templatetags'],
    version = VERSION,
    description = 'A bridge from Webpack to Django',
    long_description = README,
    long_description_content_type="text/markdown",
    author = 'Sarthak Singh',
    author_email = 'ss269@uw.edu',
    # download_url = todo,
    # url = todo,
    install_requires=[
        'Django>=2.0.0',
    ],
    keywords = ['django', 'webpack'],
    classifiers = [
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)