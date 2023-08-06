from setuptools import setup

with open('README.md', 'r') as fp:
    README = fp.read()

setup(
    name='fingerprints_matching',
    version='0.1.0',
    description='The package for fingerprints matching using minutiae matching algorithm',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Muhammad Salman Bediya',
    author_email='juraij2890@gmail.com',
    url='https://github.com/msalman2890/fingerprints_matching',
    license='MIT License',
    packages=['fingerprints_matching'],
    install_requires=[
        'opencv-python',
        'numpy'
    ],
    platforms='any',
    python_requires='>=3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
