# -----------------------------------------
# * Env *
# -----------------------------------------
import os

MOKO_PATH = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------
# * NLP *
# -----------------------------------------

# -----------------------------------------
# moko.nlp.processing
# -----------------------------------------
STOPWORD_PATH = MOKO_PATH + "/data/stopword.txt"
ADVERB_PATH = MOKO_PATH + "/data/adverb.txt"
SYNONYM_PATH = MOKO_PATH + "/data/synonym.csv"
CHARACTER_PATH = MOKO_PATH + "/data/char_synonym.txt"
CONCEPT_NOUN_PATH = MOKO_PATH + "/data/entities.csv"
USER_DICT_PATH = MOKO_PATH + "/data/user_dict.txt"

SPACING_MODEL_PATH = MOKO_PATH + "/model/soyspacing_model"
SPACING_RULE_PATH = MOKO_PATH + "/data/editorial_spacing_rules.txt"

NUM_CHAR_LIST = ['一', '壹', '二', '貳', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '萬']
PREFIX_LIST = ['其', '第']
COUNT_NOUN_LIST = ['月', '日', '百', '千', '萬', '時', '分', '人', '曰', '次', '種']
DEP_NOUN_LIST = ['等']
LAST_CHAR_LIST = ['曰']
EXCEPTION_WORD_LIST = ['平等', '少年', '靑年','中年','凶年', ]
DEMON_WORD_LIST = ['其','他','彼','此','之']

MODEL_CONFIG = {
    "hidden_size": 768,
    "dropout": 0.1,
}

VOCAB = {
    "padding_token": "[PAD]",
    "cls_token": "[CLS]",
    "sep_token": "[SEP]",
    "unk_token": "[UNK]"
}
