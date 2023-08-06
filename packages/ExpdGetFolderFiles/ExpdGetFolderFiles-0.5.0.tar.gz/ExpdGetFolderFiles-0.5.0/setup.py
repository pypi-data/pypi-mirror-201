from setuptools import setup, find_packages

setup(
    name="ExpdGetFolderFiles",
    version="0.5.0",
    author="Greg He",
    license='MIT',
    author_email="greg.he@expeditors.com",
    description="Python wrapper library for the get file list in a folder",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["loguru"],
)
