from setuptools import setup

setup(
    name='dariusVision',
    version='0.0.3',
    description='camera utilities to get last frame',
    long_description='camera utilities to get last frame',
    packages=['dariusVision'],
    install_requires=[
        'numpy',
        'opencv-python',
        'pyrealsense2',
    ],
    author='gbox3d',
    author_email='gbox3d@gmail.com',
    url='https://github.com/gbox3d/dariusVision.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)