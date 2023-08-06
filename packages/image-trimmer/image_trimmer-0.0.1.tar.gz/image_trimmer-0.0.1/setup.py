from setuptools import setup, find_packages

setup(
    name="image_trimmer",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytesseract",
        "Pillow",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": ["image_trimmer = image_trimmer.image_trimmer:main"]
    },
    url="https://github.com/jaytrairat/python-image-trimmer",
    author="jaytrairat",
    author_email="jaytrairat@outlook.com",
    description="A tool to crop images and extract text using OCR",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
