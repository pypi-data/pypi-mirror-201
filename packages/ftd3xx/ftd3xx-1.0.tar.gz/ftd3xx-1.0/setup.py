import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="ftd3xx",
    version=1.0,
    packages=setuptools.find_packages(),
    author="Future Technology Devices International Ltd.",
    description="Python interface to ftd3xx.dll using ctypes",
    keywords="ftd3xx d3xx ft60x ft600 ft601",
    url="http://www.ftdichip.com/Products/ICs/FT600.html",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"": ["*.dll"]},
)
