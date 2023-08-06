from setuptools import setup, find_packages

setup(
    name='blitzmeets',
    version='0.1.1',
    description='A utility to create virtual meetings programatically',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='youremail@example.com',
    url='https://github.com/BliyzJB/BlitzMeets',
    packages=find_packages(),
    install_requires=[
        'requests',
        'qrcode'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
