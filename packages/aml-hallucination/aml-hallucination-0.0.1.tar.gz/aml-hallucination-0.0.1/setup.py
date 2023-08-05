from setuptools import find_packages, setup

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX :: Linux'
]

setup(
    name='aml-hallucination',
    version='0.0.1',
    description='Hallucination measurement',
    long_description=open('README.txt').read() + '\n\n' +open('CHANGELOG.txt').read(),
    author='Ruby',
    author_email='zhenzhu@microsoft.com',
    license='MIT License',
    url='',
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["*.tests"]),
    install_requires=['']
)