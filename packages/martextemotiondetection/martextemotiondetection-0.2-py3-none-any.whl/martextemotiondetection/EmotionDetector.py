import os
import logging
import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer

logging.getLogger('transformers').setLevel(logging.ERROR)
logging.getLogger('transformers.file_utils').setLevel(logging.WARNING)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def set_device():
    """
    Set the device to use for TensorFlow.

    If a GPU is available, use it. Otherwise, use the CPU.

    Returns:
        str: The device to use.
    """
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        device = '/GPU:0'
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
        logging.info('Running on GPU')
    else:
        device = '/CPU:0'
        logging.info('Running on CPU')
    return device

class EmotionDetector:
    """
    A class for detecting emotions in text using the nlptown/bert-base-multilingual-uncased-sentiment model.
    """
    def __init__(self):
        """
        Initialize the EmotionDetector class.
        """
        self.tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.device = set_device()
        with tf.device(self.device):
            self.model = TFAutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    def predict(self, text):
        """
        Predict the emotion of a given text.

        Args:
            text (str): The text to predict the emotion of.

        Returns:
            list: A list of tuples containing the predicted emotion and its probability, sorted in descending order of probability.
        """
        encoded_text = self.tokenizer.encode_plus(
            text,
            max_length=128,
            add_special_tokens=True,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='tf'
        )

        with tf.device(self.device):
            prediction = self.model(encoded_text['input_ids'], encoded_text['attention_mask'])[0]
        probabilities = tf.nn.softmax(prediction, axis=1)
        labels = ['anger', 'fear', 'happy', 'love', 'neutral', 'sadness', 'surprise']
        output = list(zip(labels, probabilities.numpy()[0]))
        return sorted(output, key=lambda x: x[1], reverse=True)
