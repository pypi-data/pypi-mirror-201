from setuptools import setup, find_packages

setup(
    name='martextemotiondetection',
    version='0.2',
    description='Text Emotion Detection using Machine Learning',
    url='https://github.com/joemar25/MarTextEmotionDetection',
    author='Joemar J.',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='text emotion detection machine learning',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tensorflow',
        'transformers',
    ],
)
