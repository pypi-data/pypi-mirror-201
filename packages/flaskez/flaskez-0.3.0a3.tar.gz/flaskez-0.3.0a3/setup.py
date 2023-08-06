from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Framework :: Flask'
]

setup(
    name='flaskez',
    version='0.3.0a3',
    description='Flaskez is a multipurpose flask extension. It exists both to make creating websites easier, but also to add extra functionality to flask.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url='https://github.com/IHasBone/flaskez',
    author='IHasBone',
    author_email='info@picstreme.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['flask', 'extension', 'website', 'web', 'site', 'flask-sqlalchemy', 'database', 'sqlalchemy'],
    packages=find_packages(),
    install_requires=['flask', 'flask-sqlalchemy'],
    python_requires='>=3.7'
)
