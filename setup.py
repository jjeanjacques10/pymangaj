from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pymangaj',
    version='0.1.7',
    description='Search and download mangas.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jean Jacques Barros',
    author_email='jjean.jacques10@gmail.com',
    url='https://github.com/jjeanjacques10/pymangaj',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
