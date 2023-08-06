from setuptools import setup, find_packages

setup(
    name="hardbrake",
    version="0.0.1",
    author="Tahsin",
    author_email="hello@tahsin.us",
    description="A wrapper around HandBrake CLI for encoding multiple files with ease.",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hardbrake = src.app:main'
        ]
    }
)
