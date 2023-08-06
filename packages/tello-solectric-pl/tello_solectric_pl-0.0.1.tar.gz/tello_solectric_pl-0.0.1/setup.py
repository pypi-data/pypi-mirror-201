import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tello_solectric_pl",
    version="0.0.1",
    author="Adam Jurkiewicz",
    python_requires='>=3.8',
    author_email="adam@jurkiewicz.tech",
    description="Biblioteka dla wsparcia nauczycieli w Polsce dla dronów Tello-EDU oraz Ryzen TT (z wyświetlaczem LCD)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://solectric.pl",
    keywords='Dron Tello TelloEDU Ryzen RyzenTT DJI',
    packages=setuptools.find_packages(),
    install_requires=[
          'djitellopy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
)
