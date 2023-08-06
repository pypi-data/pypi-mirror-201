from setuptools import setup, find_packages


setup(
    name="gmap",
    version="1.5.3",
    author="Tahsin",
    author_email="your_email@example.com",
    description="A package that prints 'Hello, World!'",
    packages=find_packages(
    ),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gmap = gmap.app:main'
        ]
    }
)