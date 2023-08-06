from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="vercel_deploy",
    version="1.7",
    packages=find_packages(),
    py_modules=[ 'git_clone', 'vercel_deploy'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'git_clone = git_clone:main,vercel_deploy = vercel_deploy:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
