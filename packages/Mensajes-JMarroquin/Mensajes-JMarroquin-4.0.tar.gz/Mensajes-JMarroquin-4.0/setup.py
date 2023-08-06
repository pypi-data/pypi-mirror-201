from setuptools import setup, find_packages

setup(
    name="Mensajes-JMarroquin",
    version="4.0",
    description="Un paquete para saludar y despedir",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Jesús Marroquín",
    author_email="jesusmarro12reyes@gmail.com",
    url="https://www.instagram.com/j_marrokings/",
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suit='tests',
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.10',
    'Topic :: Utilities',
    ],

)

