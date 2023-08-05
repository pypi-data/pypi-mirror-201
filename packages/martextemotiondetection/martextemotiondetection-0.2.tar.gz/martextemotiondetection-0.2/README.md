# MarTextEmotionDetection
Used to detect emotion based on text.

### Usage
```py
detector = EmotionDetector()
output = detector.predict('I am so happy to see you!')
print(output)

# sample output:
[('neutral', 0.83419454), ('love', 0.15294598), ('happy', 0.0098365275), ('anger', 0.0016384647), ('fear', 0.0013844409)]
```
