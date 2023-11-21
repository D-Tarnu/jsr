import setuptools

setuptools.setup(
    name="jsr",
    version="0.0.1",
    author="Daniel Tarnu",
    author_email="",
    description="",
    url="",
    packages=setuptools.find_packages(),
    license="MIT",
    python_requires=">3.10",
    install_requires=[
        'numpy>=1.23.4',
        'cvxpy>=1.4.1',
        'scipy>=1.11.3'
    ]
)