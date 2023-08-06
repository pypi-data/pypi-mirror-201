from setuptools import setup, find_packages

with open('README.md', "r") as fh:
    long_description = fh.read()

def parse_requirements(fname='requirements.txt', with_version=True):
    import re
    from os.path import exists
    require_fpath = fname
    packages = []

    if exists(require_fpath):
        with open(require_fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = re.split('>=|==|>', line, maxsplit=1)
                    package = parts[0].strip()
                    packages.append(package)
    return packages

requirements = parse_requirements()
# print(requirements)
setup(
    name='trademaster406',
    version='0.0.1',
    description='TradeMaster - A platform for algorithmic trading',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='NTU_trademaster',
    author_email='TradeMaster.NTU@gmail.com',
    url='https://github.com/TradeMaster-NTU/TradeMaster',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
