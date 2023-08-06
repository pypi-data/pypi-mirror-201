columns = {
    'word': 'w.word',
    'lower': 'LOWER(w.word)',
    'lemma': 'w.lemma',
    'pos': 'w.pos',
    'xpos': 'w.xpos',
    'word_pos': 'w.word, w.pos',
    'word_xpos': 'w.word, w.xpos',
    'lower_pos': 'LOWER(w.word), w.pos',
    'lower_xpos': 'LOWER(w.word), w.xpos',
    'lemma_pos': 'w.lemma, w.pos',
    'lemma_xpos': 'w.lemma, w.xpos'
}

class Ngrams:
    def __init__(self, conn, window_size, filter, group_by, sentence_bound):
        self.conn = conn
        self.window_size = window_size
        self.filter = filter
        self.group_by = group_by
        self.sentence_bound = sentence_bound
        self.ngrams = self.get_ngrams()


    def get_ngrams(self):
        ngrams = {}

        if self.filter:
            filter_condition = self.get_filter_conditions(self.filter)
        else:
            filter_condition = ''
        c = self.conn.cursor()

        c.execute(f"""
        SELECT c.sent_index, {columns[self.group_by]} FROM corpus AS c 
        JOIN word AS w ON w.id = c.word
        {filter_condition};
        """)

        rows = c.fetchall()
        for i in range(0, len(rows)-self.window_size+1):
            ngram = rows[i:i+self.window_size]

            # Sentence Border Control
            if self.window_size > 1 and self.sentence_bound:
                same_sentence = ngram[0][0] == ngram[-1][0]
                if not same_sentence:
                    continue
            
            ngram_joined = ' '.join(['_'.join(n[1:]) for n in ngram])
            if ngram_joined not in ngrams:
                ngrams[ngram_joined] = 0
            ngrams[ngram_joined] += 1

        return dict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))
    

    def get_filter_conditions(self, filters):
        joins = []
        wheres = []
        for column, value in filters.items():
            joins.append(f'JOIN {column} ON c.{column} = {column}.id')

            if isinstance(value, list):
                sql_list = '(' + ', '.join([f"'{v}'" for v in value]) + ')'
                wheres.append(f'{column}.value IN {sql_list}')
            elif isinstance(value, str):
                wheres.append(f"{column}.value = '{value}'")
        
        filter_conditions = ' '.join(joins) + ' WHERE ' + ' AND '.join(wheres)
        return filter_conditions


    def export_as_txt(self, filename):
        with open(filename, 'w', encoding='utf-8') as file_out:
            print('ngram\tfreq', file=file_out)
            for ngram, freq in self.ngrams.items():
                print(ngram, freq, sep='\t', file=file_out)