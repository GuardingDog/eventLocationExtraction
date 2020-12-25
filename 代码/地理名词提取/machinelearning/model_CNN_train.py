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

bert_embedding = BERTEmbedding('ERNIE_1.0_max-len-512',
                               task=kashgari.LABELING,
                               sequence_length=100)

model = CNN_LSTM_Model(bert_embedding)

tf_board_callback = keras.callbacks.TensorBoard(log_dir='./logsERNIE', update_freq=1000)
eval_callback = EvalCallBack(kash_model=model,
                             valid_x=valid_x,
                             valid_y=valid_y,
                             step=5)

model.fit(train_x, train_y, valid_x, valid_y, batch_size=16, epochs=40,callbacks=[eval_callback, tf_board_callback])




model.save('location_CNN.h5')

model.evaluate(test_x, test_y)

#2 40
#3 80
#4 16 40
#5 16 80
#6 16 200