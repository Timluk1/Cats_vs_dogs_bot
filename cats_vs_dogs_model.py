import tensorflow as tf
import cv2
import numpy as np


def prediction_model(image):
    model = tf.keras.models.load_model('C:\С\model.h5')
    image = cv2.resize(image, (100, 100))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)  # Добавить размерность пакета данных

    prediction = model.predict(image)
    predicted_label = "Cat" if prediction[0][0] > 0.5 else "Dog"
    return predicted_label, prediction



