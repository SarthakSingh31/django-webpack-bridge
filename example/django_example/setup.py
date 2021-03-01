from setuptools import setup


setup(
    name = 'django-webpack-bridge-example',
    long_description_content_type="text/markdown",
    author = 'Sarthak Singh',
    author_email = 'ss269@uw.edu',
    install_requires=[
        'django-webpack-bridge @ file:///django-webpack-bridge',
    ],
    classifiers = [
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)