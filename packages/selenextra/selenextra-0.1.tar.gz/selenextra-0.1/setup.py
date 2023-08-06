from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    requires = f.readlines()
    requires = list(map(lambda x: x.strip(), requires))

setup(
    name='selenextra',
    version='0.1',
    description='Bringing additional features to Selenium',
    author='Tat Nguyen Van',
    author_email='nguyenvantat1182002@gmail.com',
    url='https://github.com/nguyenvantat1182002/SeleneXtra',
    packages=find_packages(),
    install_requires=requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
