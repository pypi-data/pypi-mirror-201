from setuptools import setup, find_packages

VERSION = '1.0.2' 
DESCRIPTION = 'JSON adapter'
LONG_DESCRIPTION = 'JSON adapters and validators for Nightingale Communication and Integration'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="nightingalejsonadapter", 
        version=VERSION,
        author="Nuno Antunes",
        author_email="<nuno.f.antunes@inov.pt>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pydantic'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['jsonadapter']
)