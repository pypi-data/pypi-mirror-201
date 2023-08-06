from .reader import *
from .create_tables import * # create_connection, create_metadata_table, create_word_table
from .insert_tables import * # insert_metadata_value
from .text_splits import parse_text
from tqdm import tqdm

spacy_taggers = {
    "en": {
        # "spacy:efficient": "en_core_web_sm",
        "spacy": "en_core_web_trf"
    },
    "de": {
        # "spacy:efficient": "de_core_news_sm",
        "spacy": "de_dep_news_trf"
    },
    "fr": {
        # "spacy:efficient": "fr_core_news_sm",
        "spacy": "fr_dep_news_trf"
    },
    "ja": {
        # "spacy:efficient": "ja_core_news_sm",
        "spacy": "ja_core_news_trf"
    }
}

class Indexer:
    def __init__(self, filename, extension, conn, tagger, lang):
        self.filename = filename
        self.extension = extension
        self.conn = conn
        self.tagger = tagger
        self.lang = lang
        self.unique_metadata = {}

        if tagger:
            if tagger.startswith('spacy'):
                import spacy
                self.nlp = spacy.load(spacy_taggers[lang][tagger], disable=['ner', 'parser'])
                self.nlp.add_pipe('sentencizer')
                self.nlp.max_length = 3000000
            elif tagger.startswith('nltk'):
                pass
            elif tagger.startswith('stanza'):
                pass
        else:
            self.nlp = None

        self.index()

    def index(self):
        if self.extension == 'TSV':
            columns, data = read_tsv(self.filename)
        elif self.extension == 'TXT':
            columns, data = read_txt(self.filename)
        elif self.extension == 'DOCX':
            columns, data = read_docx(self.filename)
        elif self.extension == 'GLOB-TXT':
            columns, data = read_glob_txt(self.filename)


        # Create a table for the language and tagger used
        create_option_table(self.conn, self.lang, self.tagger)

        # Create a table for the main corpus
        create_corpus_table(self.conn, [*columns, 'sent_index', 'word_index', 'prefix', 'suffix', 'word'])

        # Create table for each metadata column
        for column in columns:
            create_metadata_table(self.conn, column)
            self.unique_metadata[column] = {}
        create_metadata_table(self.conn, 'affix')
        self.unique_metadata['affix'] = {}

        # Create table for word
        if self.tagger == None:
            word_cols = ['word']
        else:
            word_cols = ['word', 'pos', 'xpos', 'lemma']
        create_word_table(self.conn, word_cols)
        self.unique_metadata['word'] = {}

        sent_index = 0
        for _, row in tqdm(list(data.iterrows()), colour='#522cdb'):
            # SECTION Add metadata values
            row_metadata_values = []
            for column in columns:
                value = row[column]
                value = str(value).replace("'", "''")
                if value not in self.unique_metadata[column]:
                    self.unique_metadata[column][value] = len(self.unique_metadata[column])
                    row_id = self.unique_metadata[column][value]
                    row_metadata_values.append(row_id)
                    insert_metadata_value(self.conn, column, row_id, value)
                else:
                    row_metadata_values.append(self.unique_metadata[column][value])
            # !SECTION

            # SECTION Add word values
            text = row['text']
            sentences = parse_text(text, self.tagger, self.lang, self.nlp)

            for words in sentences:
                for word_index, word in enumerate(words):
                    row_word_values = []
                    sent_index += 1
                    row_word_values.extend([sent_index, word_index])

                    # SECTION Add prefix values
                    if 'prefix' in word:
                        prefix = word['prefix']
                        if "'" in prefix:
                            prefix = prefix.replace("'", "''")
                        # if '"' in prefix:
                        #     prefix = prefix.replace('"', '""')
                        if prefix not in self.unique_metadata['affix']:
                            self.unique_metadata['affix'][prefix] = len(self.unique_metadata['affix'])
                            row_id = self.unique_metadata['affix'][prefix]
                            insert_metadata_value(self.conn, 'affix', row_id, prefix)
                            row_word_values.append(row_id)
                        else:
                            row_word_values.append(self.unique_metadata['affix'][prefix])
                    else:
                        row_word_values.append('NULL')
                    # !SECTION
                    # SECTION Add suffix values
                    if 'suffix' in word:
                        suffix = word['suffix']
                        if "'" in suffix:
                            suffix = suffix.replace("'", "''")
                        # if '"' in suffix:
                        #     suffix = suffix.replace('"', '""')
                        if suffix not in self.unique_metadata['affix']:
                            self.unique_metadata['affix'][suffix] = len(self.unique_metadata['affix'])
                            row_id = self.unique_metadata['affix'][suffix]
                            insert_metadata_value(self.conn, 'affix', row_id, suffix)
                            row_word_values.append(row_id)
                        else:
                            row_word_values.append(self.unique_metadata['affix'][suffix])
                    else:
                        row_word_values.append('NULL')
                    # !SECTION

                    # SECTION Add word values
                    full_word = word['word'].replace("'", "''") if "'" in word['word'] else word['word']

                    if self.tagger:
                        pos = word['pos']
                        xpos = word['xpos']
                        lemma = word['lemma']
                        lemma = lemma.replace("'", "''") if "'" in lemma else lemma

                    combined_word = f'{full_word}{pos}{xpos}{lemma}' if self.tagger else full_word
                    if combined_word not in self.unique_metadata['word']:
                        self.unique_metadata['word'][combined_word] = len(self.unique_metadata['word'])
                        row_id = self.unique_metadata['word'][combined_word]
                        if self.tagger:
                            insert_word_value(self.conn, 'word', row_id, [full_word, pos, xpos, lemma])
                        else:
                            insert_word_value(self.conn, 'word', row_id, [full_word])
                        row_word_values.append(row_id)
                    else:
                        row_word_values.append(self.unique_metadata['word'][combined_word])

                    insert_corpus_value(self.conn, [*columns, 'sent_index', 'word_index', 'prefix', 'suffix', 'word'],[*row_metadata_values, *row_word_values])
                    # !SECTION

        self.conn.commit()            
        # !SECTION