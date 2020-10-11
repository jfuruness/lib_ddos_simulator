from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lib_ddos_simulator',
    packages=find_packages(),
    version='0.0.4',
    author='Justin Furuness and Anna Gorbenko',
    author_email='jfuruness@gmail.com, agorbenko97@gmail.com',
    url='https://github.com/jfuruness/lib_ddos_simulator.git',
    download_url='https://github.com/jfuruness/lib_ddos.git',
    description="DDOS simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['Furuness', 'Gorbenko', 'DDOS', 'DOS', 'Simulation',
              'Sieve', 'Protag', 'KPO', 'DOSE',
              'Distributed Denial of Service',
              'Denial of Service'],
    install_requires=[
        'flasgger',
        'flask',
        'matplotlib',
        'tikzplotlib',
        'wheel',
        'setuptools',
        'tqdm',
        'pytest',
        'pathos'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': 'lib_ddos_simulator = lib_ddos_simulator.__main__:main'},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
