# AI_Cdvst

AI_Cdvst ist eine Python-Bibliothek für einfaches AI-Erstellen und -Aufnahme. Die Bibliothek bietet Funktionen zum Abspielen von WAV- und MP3-Dateien sowie zur Aufzeichnung von AI in einer WAV-Datei. Die Bibliothek enthält auch eine automatische Erkennung von Sprache. Die Dokumentation für AI_Cdvst finden Sie [hier](https://now4free.de/python/module/AI_Cdvst/documentation).

## Installation

Um AI_Cdvst zu installieren, führen Sie den folgenden Befehl aus:

```
pip install AI_Cdvst
```

## Klassen

AI_Cdvst enthält die folgenden Klassen:

| Klasse       | Beschreibung                                                                                                                                                                                                                                                                                                                                                        |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SpeechRecognizer` | Diese Klasse stellt Funktionen zur Erkennung von Sprache zur Verfügung. Mit dieser Klasse können AI-Dateien, AI-Streams oder Live-AI erkannt werden. Es ist auch möglich, eine Liste von Schlüsselwörtern einzurichten, um die Erkennung zu verbessern und zu verfeinern. Hier ist ein Beispiel, wie eine Liste von Schlüsselwörtern definiert werden kann: `recognizer.set_phrases(['hello', 'world', 'foo', 'bar'])` |
| `MicrophoneRecorder` | Diese Klasse stellt Funktionen zur Aufnahme von AI zur Verfügung. Diese Klasse ermöglicht es Ihnen, AI aufzuzeichnen und anschließend als WAV-, MP3- oder M4A-Datei zu speichern. Es ist auch möglich, das aufgezeichnete AI direkt in die Cloud hochzuladen oder in einer Datenbank zu speichern. Hier ist ein Beispiel, wie AI aufgezeichnet und als WAV-Datei gespeichert werden kann: `recorder.record_AI(record_time=5)` und `recorder.save_AI(format='wav')`. |

## Funktionen

AI_Cdvst enthält folgende Funktionen:

| Funktion                                            | Beschreibung                                                                                                                                |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `SpeechRecognizer.recognize_speech()` | Erkennt AI-Dateien, AI-Streams oder Live-AI. |
| `SpeechRecognizer.set_phrases()` | Setzt eine Liste von Schlüsselwörtern für die Erkennung. |
| `SpeechRecognizer.add_phrase()` | Fügt ein Schlüsselwort zur Liste hinzu. |
| `SpeechRecognizer.remove_phrase()` | Entfernt ein Schlüsselwort aus der Liste. |
| `MicrophoneRecorder.record_AI()` | Startet die Aufnahme des AI-Streams. |
| `MicrophoneRecorder.save_AI()` | Speichert das aufgezeichnete AI als WAV-, MP3- oder M4A-Datei. |
| `MicrophoneRecorder.upload_to_cloud()` | Lädt das aufgezeichnete AI direkt in die Cloud hoch. |
| `MicrophoneRecorder.save_to_database()` | Speichert das aufgezeichnete AI in einer Datenbank. |

## Tests

Um die Tests für AI_Cdvst auszuführen, führen Sie den folgenden Befehl aus:

```
python -m unittest discover -s tests
```

## Support

Für Fragen und Hilfe bei der Verwendung von AI_Cdvst wenden Sie sich bitte an support@now4free.de.

## Lizenz

AI_Cdvst ist lizenziert unter der MIT-Lizenz.