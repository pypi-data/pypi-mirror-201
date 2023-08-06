from setuptools import setup, find_packages

setup(
    name='musisort',
    version='1.0.1',    
    description='Automatic Music Categorization Tool',
    url='https://github.com/ReadyResearchers/AutoMusicSort',
    author='Garrison Vanzin',
    author_email='vanzing@allegheny.edu',
    license='MIT License',
    packages=['musisort', 'musisort.analysis_methods'],
    entry_points = {'console_scripts': ['musisort = musisort.main:main']},
    keywords = ['musisort'],
    install_requires=['numpy',
                      'appdirs',   
                      'scipy',  
                      'sklearn',
                      'matplotlib',
                      'librosa',  
                      'ffmpeg',
                      'progress',      
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
