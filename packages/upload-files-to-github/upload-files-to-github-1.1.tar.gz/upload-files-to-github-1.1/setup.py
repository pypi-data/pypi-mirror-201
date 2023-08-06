from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="upload-files-to-github",
    version="1.1",
    packages=find_packages(),
    py_modules=[ 'upload_files_to_github'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'upload_files_to_github = upload_files_to_github:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
