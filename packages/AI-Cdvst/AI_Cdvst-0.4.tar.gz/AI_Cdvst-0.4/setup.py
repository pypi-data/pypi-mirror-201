from setuptools import setup

setup(
    name='AI_Cdvst',
    version='0.4',
    description='Eine Python-Bibliothek zur einfachen nutzung einer AI und API callsfürai.',
    long_description="""AI_Cdvst ist eine Python-Bibliothek zur einfachen AIwiedergabe und -aufnahme. Die Bibliothek bietet Funktionen zum Abspielen von WAV- und MP3-Dateien sowie zur Aufnahme von AI in einer WAV-Datei. Die Bibliothek umfasst auch eine automatische Spracherkennungsfunktion.

Funktionen:
- Einfache Nutzung von AI
- Einfache Nutzung von API Calls
- Automatische Erkennung der Sprache des AIs

Verfügbar in Englisch und Deutsch.""",
    long_description_content_type='text/markdown',
    url='https://now4free.de/python/module/AI_Cdvst',
    author='Philipp Juen',
    author_email='support@now4free.de',
    license='MIT',
    packages=['AI_Cdvst'],
    install_requires=['openai'],
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
    keywords='AI, creating, fine tuning,  api calls, response,using',
    project_urls={'Source': 'https://github.com/philippjuen/AI_Cdvst'},
    package_data={'AI_Cdvst': ['README.md', 'README_en.md']})
