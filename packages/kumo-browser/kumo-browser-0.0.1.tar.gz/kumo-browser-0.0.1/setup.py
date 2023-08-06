from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='kumo-browser',
    version='0.0.1',
    description='A Browser library which returns content of the web page from various different webpages',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Kosta Jevtic',
    author_email='kosta.jevtic@jobcloud.ch',
    license='MIT',
    classifiers=classifiers,
    keywords='browser',
    packages=find_packages(),
    install_requires=['']
)