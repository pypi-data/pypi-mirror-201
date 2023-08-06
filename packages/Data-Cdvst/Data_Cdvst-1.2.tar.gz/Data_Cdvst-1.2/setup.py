from setuptools import setup

setup(
    name='Data_Cdvst',
    version='1.2',
    description='Eine Python-Bibliothek zur einfachen Daten mangagment datenbanken undmehr und -aufnahme.',
    long_description="""Data_Cdvst ist eine Python-Bibliothek zur einfachen nutzung von Datenbanken undeinfachen umgang mit datenverarbeitugn und -aufnahme. Die Bibliothek bietet Funktionen zum Abspielen von WAV- und MP3-Dateien sowie zur Aufnahme von Audio in einer WAV-Datei. Die Bibliothek umfasst auch eine automatische Spracherkennungsfunktion.

Funktionen:
- Einfache Datenbank erstellung
- Einfache Datenbanken Einträge erzeugen
- Einfahce Datenbanken auslesen
- Einfach Datenbanken filtern & sortieren

Verfügbar in Englisch und Deutsch.""",
    long_description_content_type='text/markdown',
    url='https://now4free.de/python/module/Data_Cdvst',
    author='Philipp Juen',
    author_email='support@now4free.de',
    license='MIT',
    packages=['Data_Cdvst'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='data, db, database, data handling, data saving, data sorting',
    project_urls={'Source': 'https://github.com/philippjuen/Audio_Cdvst'},
    package_data={'Data_Cdvst': ['README.md', 'README_en.md']})
