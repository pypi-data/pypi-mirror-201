from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="sinacor_negs",
    version="0.0.3",
    author="Renan Moretto Pereira",
    author_email="renan_morettopereira@hotmail.com",
    description="Leitor do arquivo NEGS da bolsa",
    license="MIT",
    packages=find_packages(),
    install_requires=["pandas>=2.0.0", "numpy>=1.24.2"],
    keywords=["python", "sinacor", "negs", "bolsa", "b3"],
    url="https://github.com/renanmoretto/sinacor_negs",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)