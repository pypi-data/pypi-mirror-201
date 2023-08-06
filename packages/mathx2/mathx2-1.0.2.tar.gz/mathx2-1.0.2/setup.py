from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='mathx2',
    version='1.0.2',
    description='Basic math functions',
    long_description=open('README.rst').read(),
    url='',
    author='mathx2',
    author_email='malgo.rzata.woz.niak.1999@interia.pl',
    license='MIT',
    classifiers=classifiers,
    keywords='functions math',
    packages=find_packages(),
    install_requires=[]
)
