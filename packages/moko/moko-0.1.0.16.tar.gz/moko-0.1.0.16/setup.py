from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='moko',
    version='0.1.0.16',
    description='Modern Korean NLP Package',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='yk.jeong, m.kim',
    author_email='yookyungjeong@gmail.com, munui0822@gmail.com',
    url='https://cmks.yonsei.ac.kr/cmks/database.htm?ch=2',
    license='MIT License',
    py_modules=['moko'],
    python_requires='>=3.6',
    install_requires=['soyspacing','hanja'],
    packages=['moko'],
    package_data={'moko':['data/*','model/*']}
)

