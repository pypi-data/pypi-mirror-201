from setuptools import setup, find_packages

setup(
    name='netschoool',  # Имя вашей библиотеки
    version='1.0.4',  # Версия вашей библиотеки
    description='Описание вашей библиотеки',  # Краткое описание вашей библиотеки
    author='svatoslav',  # Ваше имя
    author_email='sv14.04@mail.ru',  # Ваш email
    packages=find_packages(),  # Список пакетов, включаемых в вашу библиотеку

    classifiers=[  # Классификаторы вашей библиотеки
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
