from setuptools import setup, find_packages

setup(name='citrination-xray-scattering-integrator',
    version='0.0.3',
    url='https://github.com/slaclab/citrination-xray-scattering-integrator.git`',
    description='integrates .tif images, produces PIF records from them',
    author='Lenson A. Pellouchoud',
    author_email='lenson@slac.stanford.edu',
    packages=find_packages(),
    install_requires=[
        'pypif','pypaws','pyfai','fabio','numpy'
    ],
    entry_points={
        'citrine.dice.converter': [
            'xray_scattering_integrator = xray_scattering_integrator.integrate',
        ],
    },
)
