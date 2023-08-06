from setuptools import setup

setup(
    name='srivastav',
    version='0.0.3',    
    description='Downalerts django Middleware ',
    url='https://github.com/downalerts/django-logger',
    author='Aman Srivastav',
    author_email='amansrivastav.bytequests@gmail.com',
    license='BSD 2-clause',
    packages=['srivastav'],
    install_requires=['psutil>=5.9.4'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.5',
    ],
)