from setuptools import setup, find_packages

setup(
    name="vercel_deploy",
    version="1.4",
    packages=find_packages(),
    py_modules=[ 'git_clone', 'vercel_deploy'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'git_clone = git_clone:main,vercel_deploy = vercel_deploy:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
