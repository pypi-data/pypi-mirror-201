import re
from setuptools import setup

with open('a2d/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)[1] # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='a2d',
    author='scrazzz',
    url='https://github.com/scrazzz/a2d',
    description='Archive 4Chan threads to Discord',
    version=version,
    license='MIT',
    packages=['a2d'],
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8.0',
    entry_points={
        'console_scripts': [
            'a2d = a2d.main:cmain',
        ],
    },
)