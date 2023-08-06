import re
from operator import itemgetter
from .collocates import Collocates
from .kwic import KWIC
from .searchdist import SearchDist
from .searchwindow import SearchWindow

class Search:
    def __init__(self, conn, search_query, regex, wildcard):
        self.conn = conn
        self.search_queries = [search_query] if isinstance(search_query, str) else search_query
        self.regex = regex
        if self.regex:
            self.conn.create_function("REGEXP", 2, self.regexp)
        self.wildcard = wildcard
        self.results = self.search(self.search_queries)
        self.word_frequency = self.calculate_word_frequency(self.results)
        self.count = self.calculate_search_count(self.results)


    def search(self, search_queries):
        row_dict = {}
        for search_query in search_queries:
            search_type, parsed_search_query = self.parse_search_type(search_query)
            search_words, distance_settings, search_length = self.parse_search_query(parsed_search_query)

            uncombined = {}
            for search_word_index, search_word in enumerate(search_words):
                search_word, word_type = self.parse_word_type(search_word)
                # Normal Searches
                if search_type == 'normal':
                    if word_type == ('lower',):
                        where_condition = f'LOWER(word) IN ("{search_word}")'
                    elif word_type == ('lemma',):
                        where_condition = f'lemma IN ("{search_word}")'
                    elif word_type == ('pos',):
                        where_condition = f'pos IN ("{search_word}")'
                    elif word_type == ('lemma', 'pos'):
                        where_condition = f'(lemma IN ("{search_word[0]}")) AND (pos IN ("{search_word[1]}"))'
                    elif word_type == ('lower', 'pos'):
                        where_condition = f'(LOWER(word) IN ("{search_word[0]}")) AND (pos IN ("{search_word[1]}"))'
                # Wildcard Searches
                elif search_type == 'wildcard':
                    if word_type == ('lower',):
                        where_condition = f'id LIKE "{search_word}"'

                # RegEx Searches
                elif search_type == 'regex':
                    if word_type == ('lower',):
                        where_condition = f'id REGEXP "{search_word}"'
                c = self.conn.cursor()
                
                c.execute(f"""SELECT id FROM word WHERE {where_condition};""")
                word_ids = ','.join([str(i[0]) for i in c.fetchall()])

                c.execute(f"""
                    SELECT c.id, LOWER(w.word), w.pos, w.xpos, w.lemma FROM corpus AS c 
                    JOIN word AS w ON w.id = c.word 
                    WHERE c.word IN 
                        ({word_ids});
                    """)
                rows = c.fetchall()

                if len(search_words) == 1:
                    row_dict[search_query] = rows
                else:
                    uncombined[search_word_index] = rows

            # Merge any uncombined dict 
            if len(uncombined) > 0:
                flattened_indices = self.flatten_indices(uncombined)
                word_indices_dict = self.flatten_word_indices_meaning(uncombined)
                paired_indices = self.pair_matches(flattened_indices, distance_settings, search_length)
                paired_tuples = [(tuple(i), tuple([word_indices_dict[x] for x in i])) for i in paired_indices]
                row_dict[search_query] = paired_tuples
                combined = {}

        return row_dict


    def parse_search_type(self, search_query):
        original_query = str(search_query)
        if isinstance(search_query, str):
            search_query = search_query.split(' ')
            
            if self.regex:
                search_type = 'regex'
            elif self.wildcard:
                search_type = 'wildcard'
                search_query = [s.replace('*', '%').replace('?', '_') for s in search_query]
            else:
                search_type = 'normal'
            
        return (search_type, search_query)


    def parse_word_type(self, word):
        if '_' in word:
            word_split = word.split('_')
            if len(word_split) > 2:
                word_split = ['_'.join(word_split[0:-1]), word_split[-1]]
            # Check first word for all-caps
            if word_split[0].isupper():
                return [(word_split[0], word_split[1]), ('lemma', 'pos')]
            else:
                return [(word_split[0], word_split[1]), ('lower', 'pos')]
        else:
            if word[0] == '/' and word[-1] == '/':
                return [(word[1:-1]), ('pos',)]
            elif word.isupper():
                return [(word), ('lemma',)]
            else:
                return [(word.lower()), ('lower',)]

    def parse_search_query(self, search_words):
        # Identify any distance markers
        distance_marker_count = 0
        distance_settings = {}
        for idx, search_word in enumerate(search_words):
            # Identify distance markers
            if search_word.startswith('~') and search_word.endswith('~'):
                # The first word in search query really shouldn't start be a distance marker.
                if idx == 0 or idx == len(search_words)-1:
                    raise Exception('The first or last word in your search query should not be a distance marker.')
                else:
                    distance_settings[idx-distance_marker_count] = int(re.search(r'~(\d+)~', search_word).group(1))
                    distance_marker_count += 1
        # Remove distance markers from search_words list
        search_words = [sw for sw in search_words if not re.search(r'^~\d+~', sw)]
        search_length = len(search_words)
        # Add default distance settings to any words that didn't have a distance marker.
        for i in range(1, len(search_words)):
            if i not in distance_settings:
                distance_settings[i] = 1

        return (search_words, distance_settings, search_length)


    def regexp(self, expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None


    def flatten_indices(self, indices):
        # Takes the combined dict when searching for phrases and flattens it into a dictionary with word id -> search word index
        flattened = {}
        for k, v in indices.items():
            for i in v:
                if i[0] not in flattened:
                    flattened[i[0]] = [k]
                else:
                    flattened[i[0]].append(k)
        return dict(sorted(flattened.items(), key=lambda x: x[0]))

    
    def flatten_word_indices_meaning(self, indices):
        # Takes the combined dict when searching for phrases and flattens it into a dictionary with word id -> meaning
        return {i[0]: i[1] for k, v in indices.items() for i in v}


    def pair_matches(self, indices, distance_settings, search_length):
        final_results = []
        looking_for_hit_num = 0
        word_tracking = []
        
        for k, v in {k: v for k,v in sorted(indices.items())}.items():
            if looking_for_hit_num in v:
                if looking_for_hit_num == 0:
                    word_tracking.append(k)
                    looking_for_hit_num += 1
                else:
                    if k-word_tracking[-1] > distance_settings[looking_for_hit_num]:
                        word_tracking = []
                        looking_for_hit_num = 0
                        if looking_for_hit_num in v:
                            word_tracking.append(k)
                            looking_for_hit_num += 1
                    else:
                        word_tracking.append(k)
                        looking_for_hit_num += 1

                if looking_for_hit_num == search_length:
                    final_results.append(word_tracking)
                    word_tracking = []
                    looking_for_hit_num = 0
            else:
                word_tracking = []
                looking_for_hit_num = 0
                if 0 in v:
                    word_tracking.append(k)
                    looking_for_hit_num += 1

        return final_results

    def calculate_word_frequency(self, results):
        word_frequency = {}
        for search_query, rs in results.items():
            word_frequency[search_query] = {}
            for r in rs:
                r = r[1].lower() if isinstance(r[1], str) else ' '.join(r[1]).lower()
                if r not in word_frequency[search_query]:
                    word_frequency[search_query][r] = 0
                word_frequency[search_query][r] += 1
            word_frequency[search_query] = {k: v for k, v in sorted(word_frequency[search_query].items(), key=itemgetter(1), reverse=True)}
        return word_frequency
    

    def calculate_search_count(self, results):
        count = 0
        for search_query, rs in results.items():
            count += len(rs)
        return count


    def kwic(self, before=5, after=5, affix_sep=False, group_by='lower', show_collocates=False):
        search_window = SearchWindow(self.conn, self.results, before, after)
        return KWIC(search_window.data, affix_sep, group_by, before, after)
    

    def collocates(self, before=5, after=5, group_by='lower', stat='MI', stat_threshold=None, sample_threshold=None):
        search_window = SearchWindow(self.conn, self.results, before, after)
        return Collocates(self.conn, search_window.data, before, after, group_by, stat, stat_threshold, sample_threshold)


    def search_dist(self, group_by):
        return SearchDist(self.conn, self.results, group_by, self.search_queries)