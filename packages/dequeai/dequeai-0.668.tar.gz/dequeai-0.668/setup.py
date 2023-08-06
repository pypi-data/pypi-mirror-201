from setuptools import setup, Extension


setup(
    name='dequeai',
    version='0.00000668',
    description='Python Package for Deque AI',
    author="The Deque Team",
    author_email='team@deque.app',
    packages=["dequeai"],
    url='https://github.com/rijupahwa/deque',
    keywords='deque client for experiment tracking, sweep and other deep learning tooling',
    install_requires=[
          "coolname","requests","pillow","numpy","psutil","GPUtil","altair"
      ],
)