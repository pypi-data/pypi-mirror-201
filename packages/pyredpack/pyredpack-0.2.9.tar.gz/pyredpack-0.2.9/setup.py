import setuptools

setuptools.setup(
    name="pyredpack",
    version="0.2.9",
    license='MIT',
    author="amir taherkhani",
    author_email="amirtaherkhani@outlook.com",
    description="Serialize any python datatypes and does redis actions using redis-py",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/amirtaherkhani/PyRedPack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    install_requires=['redis>=3.4.1'],
)
