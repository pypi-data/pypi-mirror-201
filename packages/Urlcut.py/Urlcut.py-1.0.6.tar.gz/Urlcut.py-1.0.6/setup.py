from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Urlcut.py',
    version='1.0.6',
    description='Official Urlcut Public API package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://urlcut.app',
    author='Urlcut',
    author_email='support@urlcut.app',
    license='MIT',
    classifiers=classifiers,
    keywords='urlcut',
    packages=find_packages(),
    install_requires=['requests']
)
