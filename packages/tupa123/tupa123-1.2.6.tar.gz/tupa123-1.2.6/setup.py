import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tupa123',
    version='1.2.6',
    license = 'MIT',
    license_files=('LICENSE.txt',),    
    packages=['tupa123'],
    install_requires=['numpy>=1.23.5','matplotlib>=3.6.3','pandas>=1.5.3'],    
    author='Leandro Schemmer',
    author_email='leandro.schemmer@gmail.com',
    description= 'fully connected neural network with four layers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='artificial-intelligence neural-networks four-layers regression classification tupa123'
)
