from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="fake_gcp_manager_for_roy",
    version="0.1",
    packages=find_packages(),
    py_modules=[ 'fake_gcp_manager_for_roy'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'fake_gcp_manager_for_roy = fake_gcp_manager_for_roy:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
