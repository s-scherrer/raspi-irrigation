from setuptools import setup, find_packages
setup(
    name='raspi-irrigation',
    version='0.0',
    author='Samuel Scherrer',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
    ],
    # install function as script
    entry_points={
        'console_scripts': [
            'raspi-irrigation=raspi-irrigation.main:main',
        ],
    },
)
