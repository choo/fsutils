import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='fsutils',
    version='1.1.0',
    description='utility functions related to filesystems such as creating file or reading file',
    long_description=long_description,
    author='Sugimori Choo',
    author_email='sugimori.choo@gmail.com',
    url='https://github.com/choo/fsutils',
    py_modules=["fsutils"],
    install_requires=[],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
    ]
)
