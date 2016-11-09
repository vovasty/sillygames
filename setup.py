from setuptools import setup, find_packages
import os

setup(name='sillygames',
      version="0.0.1",
      description='Simple games for Cozmo',
      url='https://github.com/vovasty/sillygames',
      author='Vladimir Solomenchuk',
      author_email='vovasty@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
              'console_scripts': [
                  'sillygames = sillygames.main:main',
              ]
          },
      
      install_requires=[
          "SpeechRecognition",
          "Flask",
          "flask-socketio",
          "cozmo[camera]",
          "watchdog",
          "PyAudio",
      ],
      zip_safe=False)