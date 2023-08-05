from setuptools import setup, find_packages


setup(
    name='OpenAiChatBot',
    version='1.0',
    license='MIT',
    author="2077devwave",
    author_email='2077devwave@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/2077DevWave/OpenAiChatBot',
    keywords='openai chatbot ai image ai-bot',
    install_requires=[
          'openai',
      ],

)