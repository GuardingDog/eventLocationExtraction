import kashgari
import os
from Locating.settings import PROJECT_ROOT
import tensorflow as tf
import keras
from tensorflow.python.keras.backend import set_session

sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
loaded_model = kashgari.utils.load_model(os.path.join(PROJECT_ROOT, 'location_BILSTMCRF.h5'))
print("TESTING")
text = "我是中国人"
with graph.as_default():
    loaded_model.predict([[char for char in text]])
print("TESTING")


def model_class(text):
    global loaded_model
    global graph
    result_vec = None
    with graph.as_default():
        set_session(sess)
        result_vec = loaded_model.predict([[char for char in text]])
    return result_vec