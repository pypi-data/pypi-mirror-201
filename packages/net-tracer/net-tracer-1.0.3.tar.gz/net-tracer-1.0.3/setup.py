import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="net-tracer",
    version="1.0.3",
    author="Morbid",
    author_email="ethan.smith31415@gmail.com",
    description="A simple port scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Morbid1134/Net-Tracer",
    packages=setuptools.find_packages(),
    install_requires=[
        "nmap",
        "pyfiglet"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
