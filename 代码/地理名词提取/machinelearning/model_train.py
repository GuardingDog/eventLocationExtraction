import kashgari
from kashgari.corpus import DataReader
from kashgari.embeddings import BERTEmbedding
from kashgari.embeddings import GPT2Embedding
from kashgari.embeddings import WordEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari.tasks.labeling import CNN_LSTM_Model
from kashgari.tasks.labeling import BiLSTM_Model
import keras
from kashgari.callbacks import EvalCallBack



train_x, train_y = DataReader().read_conll_format_file('./data/Revisedlocation.train')
valid_x, valid_y = DataReader().read_conll_format_file('./data/Revisedlocation.dev')
test_x, test_y = DataReader().read_conll_format_file('./data/Revisedlocation.test')


bert_embedding = BERTEmbedding('chinese_wwm_ext_L-12_H-768_A-12',
                               task=kashgari.LABELING,
                               sequence_length=256)
# bert_embedding = WordEmbedding('news12g_bdbk20g_nov90g_dim128/news12g_bdbk20g_nov90g_dim128.model',
#                                task=kashgari.LABELING,
#                                sequence_length=100)



model = BiLSTM_CRF_Model(bert_embedding)

tf_board_callback = keras.callbacks.TensorBoard(log_dir='./logs', update_freq=1000)
eval_callback = EvalCallBack(kash_model=model,
                             valid_x=valid_x,
                             valid_y=valid_y,
                             step=5)

model.fit(train_x, train_y, valid_x, valid_y, batch_size=16, epochs=60,callbacks=[eval_callback, tf_board_callback])




model.save('REVISED_location_WordEmbedding.h5')

model.evaluate(test_x, test_y)

#2 40
#3 80
#4 16 40
#5 16 80
#6 16 200