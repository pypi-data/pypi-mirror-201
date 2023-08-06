# coding:utf-8

#from setuptools import setup
from setuptools import setup, Extension
# or
#from distutils.core import setup  

with open('README.md',encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='pyFaceTrace',   
        version='5.0.5',   
        description='easy Face Recognition for python',#long_description=foruser,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/pyFaceTrace',      
        packages=['pyFaceTrace'],   
        include_package_data=True,
        keywords = ['Face recognition', 'Face Trace'],   # Keywords that define your package best
          install_requires=[            # I get to this in a second
          'numpy',
          'scikit-image',
          'requests',
          'zipfile36',
          'bz2file'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
      ]
)
