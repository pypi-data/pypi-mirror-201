from setuptools import setup, find_packages

setup(
    name='HELML',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
    ],
    author='AlexanderJer',
    author_email='alexierusalim@gmail.com',
    description='Encoding-decoding HELML format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/dynoser/HELML/tree/master/Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
