from setuptools import setup
from os import path


top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
   name='compare_frames_g4',
   version='1.0.0',
   description='Small utils for Python',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Genzo',
   author_email='genzo@bk.ru',
   url='https://github.com/Genzo4/compare_frames',
   project_urls={
           'Bug Tracker': 'https://github.com/Genzo4/compare_frames/issues',
       },
   classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Natural Language :: Russian',
      'Topic :: Software Development',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Utilities'
   ],
   keywords=['g4',
             'compare_frames', 'compare frames',
             ],
   license='MIT',
   packages=['compare_frames_g4'],
   install_requires=['opencv-contrib-python'],
   python_requires='>=3.6'
)