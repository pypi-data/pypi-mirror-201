from math import log2
from operator import getitem
import re

group_bys = {
     'lower': 'LOWER(w.word)',
     'lemma': 'w.lemma',
     'word': 'w.word',
     'lower_pos': "LOWER(w.word) || '_' || w.pos",
     'lemma_pos': "w.lemma || '_' || w.pos",
     'word_pos': "w.word || '_' || w.pos",
}

stat_thresholds = {
    'MI': 3
}
sample_thresholds = {
    'MI': 2
}

class Collocates:
    def __init__(self, conn, search_window, before, after, group_by, stat, stat_threshold, sample_threshold):
        self.conn = conn
        self.search_window = search_window
        self.before = before
        self.after = after
        self.group_by = group_by
        self.statistic = stat
        self.stat_threshold = stat_threshold if stat_threshold else stat_thresholds[stat]
        self.sample_threshold = sample_threshold if sample_threshold else sample_thresholds[stat]

        self.collocates = self.get_collocates()


    def get_word_count(self):
        c = self.conn.cursor()
        c.execute(f'SELECT COUNT(*) FROM corpus;')
        count = c.fetchone()
        return count[0]


    def get_collocates(self):
        collocating_words = self.get_collocating_words()
        collocating_word_totals = self.get_collocating_word_totals(collocating_words)
        if self.statistic == 'MI':
            return self.collocate_by_mi(collocating_words, collocating_word_totals)
        # TODO: Add other statistics later. :)


    def get_collocating_words(self):
        collocates = {}
        for _, words in self.search_window.items():
            within_hit = False
            for word in words:
                # Stop counting collocates when word is within search query.
                if 'hit1' in word:
                    within_hit = True
                if 'hit2' in word:
                    within_hit = False
                    continue
                if within_hit:
                    continue
                
                # Get the group_by of the word.
                if self.group_by == 'lower':
                    collocate = word['lower']
                elif self.group_by == 'lemma':
                    collocate = word['lemma']
                elif self.group_by == 'word':
                    collocate = word['word']
                elif self.group_by == 'lower_pos':
                    collocate = word['lower'] + '_' + word['pos']
                elif self.group_by == 'lemma_pos':
                    collocate = word['lemma'] + '_' + word['pos']
                elif self.group_by == 'word_pos':
                    collocate = word['word'] + '_' + word['pos']
                
                if collocate not in collocates:
                    collocates[collocate] = 0
                collocates[collocate] += 1
        return collocates
    

    def get_collocating_word_totals(self, collocating_words):
        words = [f"{i}" for i in list(collocating_words.keys())]
        # Escaping words that have single quotes in them
        words = ', '.join(["'" + word.replace("'", "''") + "'" for word in words])
        # for word in words:
        #     if "'" in word:
        #         ibrk = 0
    
        c = self.conn.cursor()        
        c.execute(f"""SELECT {group_bys[self.group_by]} AS token, COUNT({group_bys[self.group_by]}) AS counter FROM corpus as c
        JOIN word AS w ON w.id = c.word
        WHERE token IN ({words})
        GROUP BY token
        ORDER BY counter DESC
        """)
        return dict(c.fetchall())
    

    def collocate_by_mi(self, word_samples, word_totals):
        friends = {}

        for word, sample in word_samples.items():
            o11 = sample
            C1 = word_totals[word]
            R1 = len(self.search_window)
            Total = self.get_word_count()
            e11 = C1 * (R1/Total)
            MI = log2(o11/e11)
            if MI >= self.stat_threshold and o11 >= self.sample_threshold:
                friends[word] = {
                    'sample': o11,
                    'total': C1,
                    'MI': round(MI, 2),
                    'expected': round(e11, 2)
                }
        return dict(sorted(friends.items(), key = lambda x: getitem(x[1], 'sample'), reverse=True))
    