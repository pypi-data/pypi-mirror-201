from itertools import groupby
import os
import re
from .create_tables import * # create_connection, create_metadata_table, create_word_table
from .indexer import Indexer
from .search import Search
from .ngrams import Ngrams
from .mattr import MATTR

class TextElixir:
    def __init__(self, filename, lang=None, tagger=None):
        self.filename = filename
        # Check to see if the file given exists.
        if not os.path.exists(self.filename):
            raise Exception(f'{filename} does not exist.')
        self.extension = re.sub(r'^.+?\.([^\.]+)$', r'\1', self.filename).upper()
        self.basename = re.sub(r'^(.+?)\.[^\.]+$', r'\1', os.path.basename(self.filename))
        self.tagger = tagger
        self.lang = lang
        self.unique_metadata = {}
        
        # Determine if the file is a tagged corpus or not.
        if not os.path.exists(f'{self.basename}.elixir'):
            self.conn = create_connection(self.basename + '.elixir')
            self.index()
        else:
            self.conn = create_connection(self.basename + '.elixir')


    
    def index(self):
        Indexer(self.filename, self.extension, self.conn, self.tagger, self.lang)


    def search(self, search_query, regex=False, wildcard=False):
        return Search(self.conn, search_query, regex, wildcard)


    def ngrams(self, window_size=1, filter=None, group_by='lower', sentence_bound=False):
        return Ngrams(self.conn, window_size, filter,  group_by, sentence_bound)

    def mattr(self, window=1000, step=1, filter=None, document=None):
        return MATTR(self.conn, window, step, filter, document)


    def get_corpus_lang(self):
        c = self.conn.cursor()
        c.execute(f"""
            SELECT lang FROM option;
        """)
        lang = c.fetchone()
        return lang[0]


    def get_corpus_tagger(self):
        c = self.conn.cursor()
        c.execute(f"""
            SELECT tagger FROM option;
        """)
        tagger = c.fetchone()
        return tagger[0]

    def get_word_count(self):
        c = self.conn.cursor()
        c.execute(f'SELECT COUNT(*) FROM corpus;')
        count = c.fetchone()
        return count[0]

    # 'word', 'pos', 'xpos', 'lemma',
    def get_word_list(self, case_sens=False):
        c = self.conn.cursor()
        case_clause = 'word' if case_sens else 'LOWER(word)'

        c.execute(f"""
            SELECT DISTINCT {case_clause} FROM word ORDER BY {case_clause};
            """)
        words = c.fetchall()
        return [w[0] for w in words]


    def get_pos_list(self):
        c = self.conn.cursor()

        c.execute(f"""
            SELECT DISTINCT pos FROM word ORDER BY pos;
            """)
        pos = c.fetchall()
        return sorted([p[0] for p in pos])


    def get_xpos_list(self):
        c = self.conn.cursor()

        c.execute(f"""
            SELECT DISTINCT xpos FROM word ORDER BY xpos;
            """)
        xpos = c.fetchall()
        return sorted([x[0] for x in xpos])

    def get_lemma_list(self):
        c = self.conn.cursor()

        c.execute(f"""
            SELECT DISTINCT lemma FROM word ORDER BY lemma;
            """)
        lemmas = c.fetchall()
        return sorted([l[0] for l in lemmas])

    def get_metadata_list(self, col):
        # Error handling
        if not isinstance(col, str):
            raise Exception(f'The `get_metadata_list` method accepts a string, not a {type(col)}.')
        
        c = self.conn.cursor()

        c.execute(f"""
            SELECT DISTINCT value FROM {col} ORDER BY value;
            """)
        rows = c.fetchall()

        return sorted([r[0] for r in rows])    

    def describe_corpus(self):
        c = self.conn.cursor()

        # Lang and Tagger
        lang = self.get_corpus_lang()
        tagger = self.get_corpus_tagger()

        print(f'This corpus consists of the {lang} language, and the {tagger} tagger was used to create it.')

        # Word Count
        c.execute('SELECT COUNT(*) FROM corpus')
        word_count = c.fetchone()[0]
        print('Token Count: {:,.0f}'.format(word_count))

        # Sentences
        c.execute('SELECT sent_index FROM corpus')
        sents = c.fetchall()
        sent_count = len(list(groupby(sents)))
        print('Sentence Count: {:,.0f}'.format(sent_count))

        # Average Words Per Sentence
        words_per_sent = round(word_count / sent_count, 1)
        print(f'Average Words Per Sentence: {words_per_sent}')

        # Metadata Columns
        c.execute('SELECT * FROM corpus')
        names = [description[0] for description in c.description]
        names = names[1:names.index('sent_index')]
        names = ', '.join(names)
        print(f'Metadata Column Names: {names}')

        # POS Values
        pos_list = ', '.join([f"'{x}'" for x in self.get_pos_list()])
        print(f'Part-of-Speech Tagset (Simple): {pos_list}')

        xpos_list = ', '.join([f"'{x}'" for x in self.get_xpos_list()])
        print(f'Part-of-Speech Tagset (Expanded): {xpos_list}')

# c.execute(f"""
#     SELECT {case_clause} as lower_word, COUNT({case_clause}) as word_count FROM corpus AS c 
#     JOIN word AS w ON w.id = c.word
#     GROUP BY lower_word
#     ORDER BY word_count DESC;
#     """)
