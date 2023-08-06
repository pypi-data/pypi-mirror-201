import os
import setuptools

def readfile(filename):
    try:
        with open(filename, 'r', encoding='latin1') as f:
            return f.read()
    except:
        return ''

version_file = os.sep.join([os.path.abspath(os.curdir), 'version.txt'])
readme_file = os.sep.join([os.path.abspath(os.curdir), 'README.md'])

print(f'version from: {version_file}')
print(f'readme from: {readme_file}')

setuptools.setup(    
    name="threadsnake",
    version=readfile(version_file),
    author="Erick Fernando Mora Ramirez",
    author_email="erickfernandomoraramirez@gmail.com",
    description="A tiny experimental server-side express-like library",
    long_description=readfile(readme_file),
    long_description_content_type="text/markdown",
    url="https://github.com/LostSavannah/threadsnake",
    project_urls={
        "Bug Tracker": "https://dev.moradev.dev/threadsnake/issues/",
        "Documentation": "https://dev.moradev.dev/threadsnake/documentation/",
        "Examples": "https://dev.moradev.dev/threadsnake/examples/",
    },
    package_data={
        "":["*.txt"]
    },
    classifiers=[
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)