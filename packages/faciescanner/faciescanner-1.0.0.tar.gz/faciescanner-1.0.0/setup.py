from setuptools import setup, find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

with open('README.md') as f:
    readme = f.read()

setup(
    name="faciescanner",
    version="1.0.0",
    author= "Xiaohu Jiang",
    email = "abeljiang2@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    description="This package is created to classify facies using borehole image array in Techlog, output prediction result.",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)