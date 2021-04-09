# -*- coding: utf-8 -*-

import codecs
import os
import pickle
import random
import re
import sys
import unittest

from tensorflow.keras import Model
import numpy as np
from sklearn.utils.validation import NotFittedError

try:
    from seq2seq_lstm import Seq2SeqLSTM
    from seq2seq_lstm.seq2seq_lstm import TextPairSequence
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from seq2seq_lstm import Seq2SeqLSTM
    from seq2seq_lstm.seq2seq_lstm import TextPairSequence


class TestSeq2SeqLSTM(unittest.TestCase):
    def setUp(self):
        self.data_set_name = os.path.join(os.path.dirname(__file__), '..', 'data', 'eng_rus_for_testing.txt')
        self.model_name = os.path.join(os.path.dirname(__file__), '..', 'data', 'seq2seq_lstm.pkl')

    def tearDown(self):
        if os.path.isfile(self.model_name):
            os.remove(self.model_name)

    def test_creation(self):
        seq2seq = Seq2SeqLSTM(batch_size=256, epochs=200, latent_dim=500, validation_split=0.1,
                              grad_clipping=50.0, lr=0.01, weight_decay=0.0001, lowercase=False, verbose=True)
        self.assertIsInstance(seq2seq, Seq2SeqLSTM)
        self.assertTrue(hasattr(seq2seq, 'batch_size'))
        self.assertEqual(seq2seq.batch_size, 256)
        self.assertTrue(hasattr(seq2seq, 'epochs'))
        self.assertEqual(seq2seq.epochs, 200)
        self.assertTrue(hasattr(seq2seq, 'latent_dim'))
        self.assertEqual(seq2seq.latent_dim, 500)
        self.assertTrue(hasattr(seq2seq, 'validation_split'))
        self.assertAlmostEqual(seq2seq.validation_split, 0.1)
        self.assertTrue(hasattr(seq2seq, 'grad_clipping'))
        self.assertAlmostEqual(seq2seq.grad_clipping, 50.0)
        self.assertTrue(hasattr(seq2seq, 'lr'))
        self.assertAlmostEqual(seq2seq.lr, 0.01)
        self.assertTrue(hasattr(seq2seq, 'weight_decay'))
        self.assertAlmostEqual(seq2seq.weight_decay, 0.0001)
        self.assertTrue(hasattr(seq2seq, 'lowercase'))
        self.assertFalse(seq2seq.lowercase)
        self.assertTrue(hasattr(seq2seq, 'verbose'))
        self.assertTrue(seq2seq.verbose)
        self.assertTrue(hasattr(seq2seq, 'random_state'))
        self.assertIsNone(seq2seq.random_state)

    def test_fit_positive01(self):
        """ Input and target texts for training are the Python tuples. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(verbose=True, lr=1e-2)
        res = seq2seq.fit(tuple(input_texts_for_training), tuple(target_texts_for_training))
        self.assertIsInstance(res, Seq2SeqLSTM)
        self.assertTrue(hasattr(res, 'input_token_index_'))
        self.assertIsInstance(res.input_token_index_, dict)
        self.assertTrue(hasattr(res, 'target_token_index_'))
        self.assertIsInstance(res.target_token_index_, dict)
        self.assertTrue(hasattr(res, 'reverse_target_char_index_'))
        self.assertIsInstance(res.reverse_target_char_index_, dict)
        self.assertTrue(hasattr(res, 'max_encoder_seq_length_'))
        self.assertIsInstance(res.max_encoder_seq_length_, int)
        self.assertGreater(res.max_encoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'max_decoder_seq_length_'))
        self.assertIsInstance(res.max_decoder_seq_length_, int)
        self.assertGreater(res.max_decoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'encoder_model_'))
        self.assertIsInstance(res.encoder_model_, Model)
        self.assertTrue(hasattr(res, 'decoder_model_'))
        self.assertIsInstance(res.decoder_model_, Model)

    def test_fit_positive02(self):
        """ Input and target texts for training are the 1-D numpy arrays. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(lr=1e-2)
        res = seq2seq.fit(np.array(input_texts_for_training), np.array(target_texts_for_training))
        self.assertIsInstance(res, Seq2SeqLSTM)
        self.assertTrue(hasattr(res, 'input_token_index_'))
        self.assertIsInstance(res.input_token_index_, dict)
        self.assertTrue(hasattr(res, 'target_token_index_'))
        self.assertIsInstance(res.target_token_index_, dict)
        self.assertTrue(hasattr(res, 'reverse_target_char_index_'))
        self.assertIsInstance(res.reverse_target_char_index_, dict)
        self.assertTrue(hasattr(res, 'max_encoder_seq_length_'))
        self.assertIsInstance(res.max_encoder_seq_length_, int)
        self.assertGreater(res.max_encoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'max_decoder_seq_length_'))
        self.assertIsInstance(res.max_decoder_seq_length_, int)
        self.assertGreater(res.max_decoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'encoder_model_'))
        self.assertIsInstance(res.encoder_model_, Model)
        self.assertTrue(hasattr(res, 'decoder_model_'))
        self.assertIsInstance(res.decoder_model_, Model)

    def test_fit_positive03(self):
        """ Input and target texts for training are the Python lists. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(lr=1e-2)
        res = seq2seq.fit(input_texts_for_training, target_texts_for_training)
        self.assertIsInstance(res, Seq2SeqLSTM)
        self.assertTrue(hasattr(res, 'input_token_index_'))
        self.assertIsInstance(res.input_token_index_, dict)
        self.assertTrue(hasattr(res, 'target_token_index_'))
        self.assertIsInstance(res.target_token_index_, dict)
        self.assertTrue(hasattr(res, 'reverse_target_char_index_'))
        self.assertIsInstance(res.reverse_target_char_index_, dict)
        self.assertTrue(hasattr(res, 'max_encoder_seq_length_'))
        self.assertIsInstance(res.max_encoder_seq_length_, int)
        self.assertGreater(res.max_encoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'max_decoder_seq_length_'))
        self.assertIsInstance(res.max_decoder_seq_length_, int)
        self.assertGreater(res.max_decoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'encoder_model_'))
        self.assertIsInstance(res.encoder_model_, Model)
        self.assertTrue(hasattr(res, 'decoder_model_'))
        self.assertIsInstance(res.decoder_model_, Model)

    def test_fit_positive04(self):
        """ Early stopping is not used in the training process. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None, lr=1e-2)
        res = seq2seq.fit(input_texts_for_training, target_texts_for_training)
        self.assertIsInstance(res, Seq2SeqLSTM)
        self.assertTrue(hasattr(res, 'input_token_index_'))
        self.assertIsInstance(res.input_token_index_, dict)
        self.assertTrue(hasattr(res, 'target_token_index_'))
        self.assertIsInstance(res.target_token_index_, dict)
        self.assertTrue(hasattr(res, 'reverse_target_char_index_'))
        self.assertIsInstance(res.reverse_target_char_index_, dict)
        self.assertTrue(hasattr(res, 'max_encoder_seq_length_'))
        self.assertIsInstance(res.max_encoder_seq_length_, int)
        self.assertGreater(res.max_encoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'max_decoder_seq_length_'))
        self.assertIsInstance(res.max_decoder_seq_length_, int)
        self.assertGreater(res.max_decoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'encoder_model_'))
        self.assertIsInstance(res.encoder_model_, Model)
        self.assertTrue(hasattr(res, 'decoder_model_'))
        self.assertIsInstance(res.decoder_model_, Model)

    def test_fit_positive05(self):
        """ Prepared evaluation set is used in the early stopping criterion. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None, lr=1e-2)
        res = seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                          eval_set=(input_texts_for_training[-20:], target_texts_for_training[-20:]))
        self.assertIsInstance(res, Seq2SeqLSTM)
        self.assertTrue(hasattr(res, 'input_token_index_'))
        self.assertIsInstance(res.input_token_index_, dict)
        self.assertTrue(hasattr(res, 'target_token_index_'))
        self.assertIsInstance(res.target_token_index_, dict)
        self.assertTrue(hasattr(res, 'reverse_target_char_index_'))
        self.assertIsInstance(res.reverse_target_char_index_, dict)
        self.assertTrue(hasattr(res, 'max_encoder_seq_length_'))
        self.assertIsInstance(res.max_encoder_seq_length_, int)
        self.assertGreater(res.max_encoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'max_decoder_seq_length_'))
        self.assertIsInstance(res.max_decoder_seq_length_, int)
        self.assertGreater(res.max_decoder_seq_length_, 0)
        self.assertTrue(hasattr(res, 'encoder_model_'))
        self.assertIsInstance(res.encoder_model_, Model)
        self.assertTrue(hasattr(res, 'decoder_model_'))
        self.assertIsInstance(res.decoder_model_, Model)

    def test_fit_negative01(self):
        """ Object with input texts is not one of the basic sequence types. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape(f'`{type({1, 2})}` is wrong type for `X`.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(set(input_texts_for_training), target_texts_for_training)

    def test_fit_negative02(self):
        """ Object with target texts is not one of the basic sequence types. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape(f'`{type({1, 2})}` is wrong type for `y`.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training, set(target_texts_for_training))

    def test_fit_negative03(self):
        """ Number of input texts does not equal to number of target texts. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape(f'`X` does not correspond to `y`! {len(input_texts_for_training)} != {len(target_texts_for_training) - 1}.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training, target_texts_for_training[:-1])

    def test_fit_negative04(self):
        """ Some parameter of the `Seq2SeqLSTM` object is wrong. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(batch_size=0)
        true_err_msg = re.escape('`batch_size` must be a positive number! 0 is not positive.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training, target_texts_for_training)

    def test_fit_negative05(self):
        """ Special evaluation set is neither list nor tuple. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None)
        true_err_msg = re.escape(f'`eval_set` must be `{type((1, 2))}` or `{type([1, 2])}`, not `{type({1: "a", 2: "b"})}`!')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                        eval_set={'X': input_texts_for_training[-20:], 'y': target_texts_for_training[-20:]})

    def test_fit_negative06(self):
        """ Special evaluation set is not a two-element tuple. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None)
        true_err_msg = re.escape('`eval_set` must be a two-element sequence! 3 != 2')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                        eval_set=(input_texts_for_training[-20:], target_texts_for_training[-20:], [3, 4]))

    def test_fit_negative07(self):
        """ Object with input texts in the special evaluation set is not one of the basic sequence types. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape(f'`{type({1, 2})}` is wrong type for `X_eval_set`.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                        eval_set=(set(input_texts_for_training[-20:]), target_texts_for_training[-20:]))

    def test_fit_negative08(self):
        """ Object with target texts in the special evaluation set is not one of the basic sequence types. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape(f'`{type({1, 2})}` is wrong type for `y_eval_set`.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                        eval_set=(input_texts_for_training[-20:], set(target_texts_for_training[-20:])))

    def test_fit_negative09(self):
        """ Number of input texts does not equal to number of target texts in the special evaluation set. """
        input_texts_for_training, target_texts_for_training = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM()
        true_err_msg = re.escape('`X_eval_set` does not correspond to `y_eval_set`! 20 != 19.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            seq2seq.fit(input_texts_for_training[:-20], target_texts_for_training[:-20],
                        eval_set=(input_texts_for_training[-20:], target_texts_for_training[-19:]))

    def test_predict_positive001(self):
        """ Part of correctly predicted texts must be greater than 0.1. """
        input_texts, target_texts = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None, epochs=200, lr=1e-2, verbose=True, lowercase=False)
        predicted_texts = seq2seq.fit_predict(input_texts, target_texts)
        self.assertIsInstance(predicted_texts, list)
        self.assertEqual(len(predicted_texts), len(input_texts))
        indices = list(range(len(predicted_texts)))
        random.shuffle(indices)
        print('')
        print('Some predicted texts:')
        for ind in range(min(5, len(predicted_texts))):
            print('    True: ' + self.detokenize_text(target_texts[indices[ind]]) +
                  '\t Predicted: ' + self.detokenize_text(predicted_texts[indices[ind]]))
        self.assertGreater(self.estimate(predicted_texts, target_texts), 0.0001)

    def test_predict_negative001(self):
        """ Usage of the seq2seq model for prediction without training. """
        input_texts_for_testing, _ = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None, epochs=20)
        with self.assertRaises(NotFittedError):
            _ = seq2seq.predict(input_texts_for_testing)

    def test_predict_negative002(self):
        """ Input texts for prediction are wrong. """
        input_texts_for_testing, target_texts_for_testing = self.load_text_pairs(self.data_set_name)
        seq2seq = Seq2SeqLSTM(validation_split=None, epochs=20)
        seq2seq.fit(input_texts_for_testing, target_texts_for_testing)
        true_err_msg = re.escape(f'`{type({1, 2})}` is wrong type for `X`.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            _ = seq2seq.predict(set(input_texts_for_testing))

    def test_check_X_negative001(self):
        """ All texts must be a string and have a `split` method. """
        texts = ['123', 4, '567']
        true_err_msg = re.escape('Sample 1 of `X` is wrong! This sample have not the `split` method.')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            Seq2SeqLSTM.check_X(texts, 'X')

    def test_check_X_negative002(self):
        """ If list of texts is specified as the NumPy array, then it must be a 1-D array. """
        texts = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
        true_err_msg = re.escape('`X` must be a 1-D array!')
        try:
            checking_method = self.assertRaisesRegex
        except:
            checking_method = self.assertRaisesRegexp
        with checking_method(ValueError, true_err_msg):
            Seq2SeqLSTM.check_X(texts, 'X')

    def test_serialize_untrained(self):
        seq2seq = Seq2SeqLSTM(batch_size=256, epochs=200, latent_dim=500, validation_split=0.1,
                              grad_clipping=50.0, lr=0.01, weight_decay=0.0001, lowercase=False, verbose=True,
                              random_state=42)
        with open(self.model_name, 'wb') as fp:
            pickle.dump(seq2seq, fp)
        with open(self.model_name, 'rb') as fp:
            another_seq2seq = pickle.load(fp)
        self.assertIsInstance(another_seq2seq, Seq2SeqLSTM)
        self.assertTrue(hasattr(another_seq2seq, 'batch_size'))
        self.assertEqual(another_seq2seq.batch_size, 256)
        self.assertTrue(hasattr(another_seq2seq, 'epochs'))
        self.assertEqual(another_seq2seq.epochs, 200)
        self.assertTrue(hasattr(another_seq2seq, 'latent_dim'))
        self.assertEqual(another_seq2seq.latent_dim, 500)
        self.assertTrue(hasattr(another_seq2seq, 'validation_split'))
        self.assertAlmostEqual(another_seq2seq.validation_split, 0.1)
        self.assertTrue(hasattr(another_seq2seq, 'grad_clipping'))
        self.assertAlmostEqual(another_seq2seq.grad_clipping, 50.0)
        self.assertTrue(hasattr(another_seq2seq, 'lr'))
        self.assertAlmostEqual(another_seq2seq.lr, 0.01)
        self.assertTrue(hasattr(another_seq2seq, 'weight_decay'))
        self.assertAlmostEqual(another_seq2seq.weight_decay, 0.0001)
        self.assertTrue(hasattr(another_seq2seq, 'lowercase'))
        self.assertFalse(another_seq2seq.lowercase)
        self.assertTrue(hasattr(another_seq2seq, 'verbose'))
        self.assertTrue(another_seq2seq.verbose)
        self.assertTrue(hasattr(another_seq2seq, 'random_state'))
        self.assertEqual(another_seq2seq.random_state, 42)

    def test_serialize_trained(self):
        input_texts, target_texts = self.load_text_pairs(self.data_set_name)
        indices = list(range(len(input_texts)))
        random.shuffle(indices)
        n = int(round(0.2 * len(indices)))
        input_texts_for_training = []
        target_texts_for_training = []
        for ind in indices[:-n]:
            input_texts_for_training.append(input_texts[ind])
            target_texts_for_training.append(target_texts[ind])
        input_texts_for_testing = []
        target_texts_for_testing = []
        for ind in indices[-n:]:
            input_texts_for_testing.append(input_texts[ind])
            target_texts_for_testing.append(target_texts[ind])
        seq2seq = Seq2SeqLSTM(validation_split=None, epochs=10, lr=1e-3)
        seq2seq.fit(input_texts_for_training, target_texts_for_training,
                    eval_set=(input_texts_for_testing, target_texts_for_testing))
        predicted_texts_1 = seq2seq.predict(input_texts_for_testing)
        with open(self.model_name, 'wb') as fp:
            pickle.dump(seq2seq, fp)
        del seq2seq
        with open(self.model_name, 'rb') as fp:
            another_seq2seq = pickle.load(fp)
        predicted_texts_2 = another_seq2seq.predict(input_texts_for_testing)
        self.assertEqual(predicted_texts_1, predicted_texts_2)

    def test_tokenize_text_positive01(self):
        """ Tokenization with saving of the characters register. """
        src = 'a\t B  c Мама мыла \n\r раму 1\n'
        dst_true = ['a', 'B', 'c', 'Мама', 'мыла', 'раму', '1']
        dst_predicted = Seq2SeqLSTM.tokenize_text(src, lowercase=False)
        self.assertEqual(dst_predicted, dst_true)

    def test_tokenize_text_positive02(self):
        """ Tokenization with bringing the resulting tokens to lowercase. """
        src = 'a\t B  c Мама мыла \n\r раму 1\n'
        dst_true = ['a', 'b', 'c', 'мама', 'мыла', 'раму', '1']
        dst_predicted = Seq2SeqLSTM.tokenize_text(src, lowercase=True)
        self.assertEqual(dst_predicted, dst_true)

    @staticmethod
    def load_text_pairs(file_name):
        input_texts = list()
        target_texts = list()
        line_idx = 1
        with codecs.open(file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
            cur_line = fp.readline()
            while len(cur_line) > 0:
                prep_line = cur_line.strip()
                if len(prep_line) > 0:
                    err_msg = f'File "{file_name}": line {line_idx} is wrong!'
                    line_parts = prep_line.split('\t')
                    assert len(line_parts) == 2, err_msg
                    new_input_text = line_parts[0].strip()
                    new_target_text = line_parts[1].strip()
                    assert (len(new_input_text) > 0) and (len(new_target_text) > 0), err_msg
                    input_texts.append(TestSeq2SeqLSTM.tokenize_text(new_input_text))
                    target_texts.append(TestSeq2SeqLSTM.tokenize_text(new_target_text))
                cur_line = fp.readline()
                line_idx += 1
        return input_texts, target_texts

    @staticmethod
    def tokenize_text(src):
        tokens = list()
        for cur in src.split():
            tokens += list(cur)
            tokens.append('<space>')
        return ' '.join(tokens[:-1])

    @staticmethod
    def detokenize_text(src):
        new_text = ''
        for cur_token in src.split():
            if cur_token == '<space>':
                new_text += ' '
            else:
                new_text += cur_token
        return new_text.strip()

    @staticmethod
    def estimate(predicted_texts, true_texts):
        n_corr = 0
        n_total = len(predicted_texts)
        for i in range(n_total):
            cur_predicted = TestSeq2SeqLSTM.detokenize_text(predicted_texts[i]).lower()
            cur_true = TestSeq2SeqLSTM.detokenize_text(true_texts[i]).lower()
            if cur_predicted == cur_true:
                n_corr += 1
        return n_corr / float(n_total)


class TestTextPairSequence(unittest.TestCase):
    def test_generate_data_for_training(self):
        input_texts = [
            'a b c',
            'a c',
            '0 1 b',
            'b a',
            'b c'
        ]
        target_texts = [
            'а б а 2',
            '2 3',
            'а б а',
            'б а',
            'б 3'
        ]
        batch_size = 2
        max_encoder_seq_length = 3
        max_decoder_seq_length = 6
        input_token_index = {'0': 0, '1': 1, 'a': 2, 'b': 3, 'c': 4}
        target_token_index = {'\t': 0, '\n': 1, '2': 2, '3': 3, 'а': 4, 'б': 5}
        true_batches = [
            (
                [
                    np.array([
                        [
                            [0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0]
                        ],
                        [
                            [0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0]
                        ]
                    ]),
                    np.array([
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
                        ],
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        ]
                    ])
                ],
                np.array([
                    [
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ],
                    [
                        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ]
                ])
            ),
            (
                [
                    np.array([
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0]
                        ],
                        [
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0]
                        ]
                    ]),
                    np.array([
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                        ],
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                        ]
                    ])
                ],
                np.array([
                    [
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ],
                    [
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ]
                ])
            ),
            (
                [
                    np.array([
                        [
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0]
                        ],
                        [
                            [0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0]
                        ]
                    ]),
                    np.array([
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                        ],
                        [
                            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
                        ]
                    ])
                ],
                np.array([
                    [
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ],
                    [
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    ]
                ])
            )
        ]
        training_set_generator = TextPairSequence(
            input_texts=input_texts, target_texts=target_texts, batch_size=batch_size,
            max_encoder_seq_length=max_encoder_seq_length, max_decoder_seq_length=max_decoder_seq_length,
            input_token_index=input_token_index, target_token_index=target_token_index, lowercase=False
        )
        self.assertIsInstance(training_set_generator, TextPairSequence)
        self.assertTrue(hasattr(training_set_generator, 'input_texts'))
        self.assertTrue(hasattr(training_set_generator, 'target_texts'))
        self.assertTrue(hasattr(training_set_generator, 'batch_size'))
        self.assertTrue(hasattr(training_set_generator, 'max_encoder_seq_length'))
        self.assertTrue(hasattr(training_set_generator, 'max_decoder_seq_length'))
        self.assertTrue(hasattr(training_set_generator, 'input_token_index'))
        self.assertTrue(hasattr(training_set_generator, 'target_token_index'))
        self.assertTrue(hasattr(training_set_generator, 'lowercase'))
        self.assertTrue(hasattr(training_set_generator, 'n_text_pairs'))
        self.assertTrue(hasattr(training_set_generator, 'n_batches'))
        self.assertIs(training_set_generator.input_texts, input_texts)
        self.assertIs(training_set_generator.target_texts, target_texts)
        self.assertEqual(training_set_generator.batch_size, batch_size)
        self.assertEqual(training_set_generator.max_encoder_seq_length, max_encoder_seq_length)
        self.assertEqual(training_set_generator.max_decoder_seq_length, max_decoder_seq_length)
        self.assertIs(training_set_generator.input_token_index, input_token_index)
        self.assertIs(training_set_generator.target_token_index, target_token_index)
        self.assertFalse(training_set_generator.lowercase)
        self.assertIsInstance(training_set_generator.n_text_pairs, int)
        self.assertEqual(training_set_generator.n_text_pairs, len(input_texts))
        self.assertIsInstance(training_set_generator.n_batches, int)
        self.assertEqual(training_set_generator.n_batches, len(true_batches))
        for batch_ind in range(len(true_batches)):
            predicted_batch = training_set_generator[batch_ind]
            self.assertIsInstance(predicted_batch, tuple, msg=f'batch_ind={batch_ind}')
            self.assertEqual(len(predicted_batch), 2, msg=f'batch_ind={batch_ind}')
            self.assertIsInstance(predicted_batch[0], list, msg=f'batch_ind={batch_ind}')
            self.assertIsInstance(predicted_batch[1], np.ndarray, msg=f'batch_ind={batch_ind}')
            self.assertEqual(len(predicted_batch[0]), 2, msg=f'batch_ind={batch_ind}')
            self.assertIsInstance(predicted_batch[0][0], np.ndarray, msg=f'batch_ind={batch_ind}')
            self.assertIsInstance(predicted_batch[0][1], np.ndarray, msg=f'batch_ind={batch_ind}')
            self.assertTrue(np.array_equal(predicted_batch[0][0], true_batches[batch_ind][0][0]),
                            msg=f'batch_ind={batch_ind}, encoder_input_data')
            self.assertTrue(np.array_equal(predicted_batch[0][1], true_batches[batch_ind][0][1]),
                            msg=f'batch_ind={batch_ind}, decoder_input_data')
            self.assertTrue(np.array_equal(predicted_batch[1], true_batches[batch_ind][1]),
                            msg=f'batch_ind={batch_ind}, decoder_target_data')


if __name__ == '__main__':
    unittest.main(verbosity=2)
