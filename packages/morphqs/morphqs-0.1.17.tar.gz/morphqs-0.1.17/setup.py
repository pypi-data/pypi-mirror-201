import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Jared Lutgen",
    author_email="jlutgen@morpheusdata.com",
    name='morphqs',
    license="MIT",
    description='Tool utilized to deploy some basic concepts for the Morpheus Data Platform',
    version='v0.1.17',
    long_description=README,
    url='https://gitlab.com/jaredlutgen/morphqs',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)