class SearchWindow:
    def __init__(self, conn, results, before, after):
        self.conn = conn
        self.results = results
        self.before = before
        self.after = after
        self.data = self.get_search_window()


    def get_search_window(self):
        ranges = self.get_full_ranges(self.results)
        values = ', '.join([str(num) for key, r in ranges.items() for num in r])
        kwic_word_ids = self.get_kwic_word_ids(values)
        word_ids = ', '.join(str(v[0]) for k, v in kwic_word_ids.items())
        word_data = self.get_word_data(word_ids)
        affix_data = self.get_affix_data()

        data = {}
        for key, values in ranges.items():
            key_first = key[0] if isinstance(key, tuple) else key
            key_last = key[1] if isinstance(key, tuple) else key
 
            words = []
            for value in values:
                word_values = None
                word_values = dict(word_data[kwic_word_ids[value][0]])
                word_values['prefix'] = affix_data[kwic_word_ids[value][1]]
                word_values['suffix'] = affix_data[kwic_word_ids[value][2]]

                if '.' in word_values['suffix']:
                    ibrk = 0
                if value == key_first:
                    word_values['hit1'] = True
                if value == key_last:
                    word_values['hit2'] = True
                words.append(word_values)
            data[key] = words

        return data
        

    def get_kwic_word_ids(self, values):
        c = self.conn.cursor()
        c.execute(f"""SELECT id, word, prefix, suffix FROM corpus WHERE id in ({values});
            """)
        rows = c.fetchall()
        # 1 = word_id, #2 = prefix, #3 = suffix
        data_dict = {row[0]: tuple(row[1:len(row)]) for row in rows}

        return data_dict
    
    
    def get_word_data(self, values):
        c = self.conn.cursor()
        c.execute(f"""
            SELECT id, word, LOWER(word), pos, lemma
            FROM word
            WHERE id in ({values});
        """)

        rows = c.fetchall()
        data_dict = {}
        for row in rows:
            data_dict[row[0]] = {
                'word': row[1],
                'lower': row[2],
                'pos': row[3],
                'lemma': row[4]
            }
        return data_dict


    def get_affix_data(self):
        c = self.conn.cursor()
        c.execute(f"""
            SELECT *
            FROM affix
        """)

        rows = c.fetchall()
        data_dict = {}
        for row in rows:
            data_dict[row[0]] = row[1]
        data_dict[None] = ''
        return data_dict


    def get_full_ranges(self, results):
        total_rows = self.count_total_rows('corpus')

        ranges = {}
        for _, result_tuples in results.items():
            for result_tuple in result_tuples:
                key_first = result_tuple[0][0] if isinstance(result_tuple[0], tuple) else result_tuple[0]
                key_last = result_tuple[0][-1] if isinstance(result_tuple[0], tuple) else result_tuple[0]
                numbers = list(range(key_first-self.before, key_last+self.after+1))
                numbers = [num for num in numbers if num > 0 and num <= total_rows]
                if (key_first, key_last) not in ranges:
                    ranges[(key_first, key_last)] = []
                ranges[(key_first, key_last)].extend(numbers)
        return ranges


    def count_total_rows(self, table):
        c = self.conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {table};")
        return c.fetchone()[0]
