from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pydocedit',
    version='0.0.6',
    description='A package to take edit doc/docx/trf files.',
    author= 'Ateendra Jha',
    author_email="ateendrajha@live.com",
    url = 'https://www.drateendrajha.com/projects/pydocedit',
    long_description_content_type="text/markdown",
    long_description = long_description,
    packages=setuptools.find_packages(),
    keywords=['video', 'images', 'video2images', "image crop"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pydocedit'],
    package_dir={'':'src'},
    install_requires = [
        'regex',
        'comtypes',
        'pillow',
        'python-docx',
        'nltk',
        'pywin32',
        'glob2'
    ]
)