from setuptools import setup, find_packages

setup(
    name="vercel-deploy",
    version="1.0",
    packages=find_packages(),
    py_modules=[ 'git_clone', 'vercel_deploy'],
    install_requires=[],
)
