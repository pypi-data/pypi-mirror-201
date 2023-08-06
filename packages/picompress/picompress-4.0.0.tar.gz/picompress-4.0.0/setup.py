import setuptools

setuptools.setup(
    name="picompress",
    version="4.0.0",
    description="python compression lib",
    packages=['picompress'],
    package_data={'picompress': ['so/*', 'dll/*']},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
