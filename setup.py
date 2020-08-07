from setuptools import setup, find_packages
setup(
    name='raspi-irrigation',
    version='0.0',
    author='Samuel Scherrer',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "flask",
    ],
    # install function as script
    entry_points={
        'console_scripts': [
            'run-irrigation=raspi_irrigation.main:main',
        ],
    },
)
