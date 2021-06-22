from setuptools import setup


def readme():
    with open('README.rst') as file:
        return file.read()


setup(
    name='streams',
    author='Tyler Crompton',
    author_email='tyler@tylercrompton.com',
    version='0.0.0',
    description='Provides stream classes inspired by Scheme',
    long_description=readme(),
    license='GPLv3',
    url='https://github.com/tylercrompton/streams',
    keywords='stream streams lazy evaluation cons scheme haskell',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    packages=('streams',),
    include_package_data=True,
    zip_safe=True,
)
