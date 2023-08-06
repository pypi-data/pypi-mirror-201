from setuptools import setup

setup(
    name='rda-apps-clients',
    version='0.1.0',
    description='Python Client to interact with Research Data Archive\'s API',
    author='Riley Conroy',
    url='https://github.com/NCAR/rda-apps-clients',
    author_email='rpconroy@ucar.edu',
    install_requires=[
        'requests',
    ],
    entry_points={
    'console_scripts': [
        'rdams_client = rda_apps_clients.rdams_client:main',
    ],
},
)
