from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
  long_description = fh.read()
  
setup(
  name='py3enc',
  packages=find_packages(),
  include_package_data=True,
  version="1.0.0",
  description= 'Simple module forn encrypt python3 scripts.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='0xakxvau',
  author_email='0xakxvau@gmail.com',
  install_requires=["pytz"],
  keywords=["python","pyenc","encpy","python encrypt","python encryption","encpy python","py3enc"],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Environment :: Console'],
  license='MIT',
  python_requires='>=3.9.5'
  )