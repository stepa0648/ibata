from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='ibata',
    version='0.0.4',
    description='A tool for analyzing bank transactions',
    long_description=long_description,
    author='stepa0648',
    keywords='cli, bank, transaction',
    summary='A tool for analyzing bank transactions',
    license='MIT',
    packages=find_packages(),
    package_data={'tests': ['tests']},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
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
