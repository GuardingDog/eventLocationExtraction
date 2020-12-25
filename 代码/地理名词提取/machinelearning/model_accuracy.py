import kashgari
from kashgari.corpus import DataReader
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari.tasks.labeling import CNN_LSTM_Model
from kashgari.tasks.labeling import BiLSTM_Model
import keras
from kashgari.callbacks import EvalCallBack

train_x, train_y = DataReader().read_conll_format_file('./data/location.train')
valid_x, valid_y = DataReader().read_conll_format_file('./data/location.dev')
test_x, test_y = DataReader().read_conll_format_file('./data/location.test')


# model = kashgari.utils.load_model('location_BILSTM.h5')
# model.evaluate(test_x, test_y)
# model = kashgari.utils.load_model('location_CNN.h5')
# model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo7.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo6.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo5.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo4.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo3.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow_demo2.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_nerow.h5')
model.evaluate(test_x, test_y)
model = kashgari.utils.load_model('location_BILSTMCRF.h5')
model.evaluate(test_x, test_y)