import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypg-cdc",
    version="0.0.1",
    author="sjy",
    author_email="",
    description="PostgreSQL CDC library using pgoutput and python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sshd123/pypgoutput",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
          'psycopg2',
          'pydantic',
    ],
)
