from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="image-trimmer",
    version="0.0.10",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytesseract",
        "Pillow",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": ["image-trimmer = image_trimmer.image_trimmer:main"]
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jaytrairat/python-image-trimmer",
    author="jaytrairat",
    author_email="jaytrairat@outlook.com",
    description="A tool to crop images and extract text using OCR",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
