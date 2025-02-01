from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as fd:
    requirements = fd.read().splitlines()


setup(
    name="gruvbox-factory",
    packages=["factory"],
    version="1.1.0",
    license="MIT",
    author="Paulo Pacitti",
    author_email="ppacitti@outlook.com",
    url="https://github.com/paulopacitti/gruvbox-factory",
    description="convert any image to the gruvbox pallete!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["gruvbox-factory= factory.__main__:main"]},
    include_package_data=True,
    install_requires=requirements,
    keywords=[
        "gruvbox",
        "cli",
        "gruvbox-factory",
        "wallpaper",
        "image",
        "image-go-nord",
        "palette",
        "factory",
        "nord",
    ],
)
