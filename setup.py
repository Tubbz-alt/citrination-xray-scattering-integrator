from setuptools import setup, find_packages

setup(name='citrination_integrator',
    version='0.0.1',
    url='https://github.com/slaclab/citrination_integrator.git`',
    description='integrates .tif images, produces PIF records from them',
    author='Lenson A. Pellouchoud',
    author_email='lenson@slac.stanford.edu',
    packages=find_packages(),
    install_requires=[
        'pypif','pypaws','pyfai','tifffile'
    ],
    entry_points={
        'citrine.dice.converter': [
            'scattering_integrator = citrination_integrator.integrate',
        ],
    },
)
