from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='ibata',
    version='0.0.4',
    description='A tool for analyzing bank transactions',
    long_description=long_description,
    author='Štěpán Severa',
    author_email='severste@fit.cvut.cz',
    keywords='cli, bank, transaction',
    summary='A tool for analyzing bank transactions',
    license='CC0',
    packages=find_packages(),
    package_data={'tests': ['tests']},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ibata = ibata.ibata:main',
        ],
    },
    install_requires=['click', 'requests', 'matplotlib'],
    extras_require={
        "test": ['pytest', 'flexmock', 'betamax'],
    }
)
