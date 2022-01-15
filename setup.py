import setuptools

with open ("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "pollenflug",
    version = "0.1",
    scripts = ["pollenflug"],
    author = "Bader Zaidan",
    author_email = "bader.zaidan@rwth-aachen.de",
    description = "CLI allergy forecast tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/BaderSZ/pollenflug",
    packages=setuptools.find_packages(),
    platforms=["Linux", "Darwin", "Windows"],
    license="GPLv3+",
    license_files=["LICENSE"],
    install_requires=["requests"],
    classifiers =[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
