from setuptools import setup

setup(
    name='vcframe',
    version='1.0.2',    
    description='Work with VCF files as pandas DataFrames',
    url='https://github.com/sudogene/vcframe',
    author='Andy Wu',
    author_email='andyuwub@gmail.com',
    license='',
    packages=['vcframe'],
    install_requires=['pandas>=1.5.3'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',  
        'Operating System :: OS Independent',        
        'Programming Language :: Python :: 3'
    ],
)