# Data_Cdvst

Audio_Cdvst ist eine Python-Bibliothek für einfaches Audio-Playback und -Aufnahme. Die Bibliothek bietet Funktionen zum Abspielen von WAV- und MP3-Dateien sowie zur Aufzeichnung von Audio in einer WAV-Datei. Die Bibliothek enthält auch eine automatische Erkennung von Sprache. Die Dokumentation für Audio_Cdvst finden Sie [hier](https://now4free.de/python/module/Audio_Cdvst/documentation).

## Installation

Um Audio_Cdvst zu installieren, führen Sie den folgenden Befehl aus:

```
pip install Audio_Cdvst
```

## Klassen

Audio_Cdvst enthält die folgenden Klassen:

| Klasse       | Beschreibung                                                                                                                                                                                                                                                                                                                                                        |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SpeechRecognizer` | Diese Klasse stellt Funktionen zur Erkennung von Sprache zur Verfügung. Mit dieser Klasse können Audio-Dateien, Audio-Streams oder Live-Audio erkannt werden. Es ist auch möglich, eine Liste von Schlüsselwörtern einzurichten, um die Erkennung zu verbessern und zu verfeinern. Hier ist ein Beispiel, wie eine Liste von Schlüsselwörtern definiert werden kann: `recognizer.set_phrases(['hello', 'world', 'foo', 'bar'])` |
| `MicrophoneRecorder` | Diese Klasse stellt Funktionen zur Aufnahme von Audio zur Verfügung. Diese Klasse ermöglicht es Ihnen, Audio aufzuzeichnen und anschließend als WAV-, MP3- oder M4A-Datei zu speichern. Es ist auch möglich, das aufgezeichnete Audio direkt in die Cloud hochzuladen oder in einer Datenbank zu speichern. Hier ist ein Beispiel, wie Audio aufgezeichnet und als WAV-Datei gespeichert werden kann: `recorder.record_audio(record_time=5)` und `recorder.save_audio(format='wav')`. |

## Funktionen

Audio_Cdvst enthält folgende Funktionen:

| Funktion                                            | Beschreibung                                                                                                                                |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `SpeechRecognizer.recognize_speech()` | Erkennt Audio-Dateien, Audio-Streams oder Live-Audio. |
| `SpeechRecognizer.set_phrases()` | Setzt eine Liste von Schlüsselwörtern für die Erkennung. |
| `SpeechRecognizer.add_phrase()` | Fügt ein Schlüsselwort zur Liste hinzu. |
| `SpeechRecognizer.remove_phrase()` | Entfernt ein Schlüsselwort aus der Liste. |
| `MicrophoneRecorder.record_audio()` | Startet die Aufnahme des Audio-Streams. |
| `MicrophoneRecorder.save_audio()` | Speichert das aufgezeichnete Audio als WAV-, MP3- oder M4A-Datei. |
| `MicrophoneRecorder.upload_to_cloud()` | Lädt das aufgezeichnete Audio direkt in die Cloud hoch. |
| `MicrophoneRecorder.save_to_database()` | Speichert das aufgezeichnete Audio in einer Datenbank. |

## Tests

Um die Tests für Audio_Cdvst auszuführen, führen Sie den folgenden Befehl aus:

```
python -m unittest discover -s tests
```

## Support

Für Fragen und Hilfe bei der Verwendung von Audio_Cdvst wenden Sie sich bitte an support@now4free.de.

## Lizenz

Audio_Cdvst ist lizenziert unter der MIT-Lizenz.

