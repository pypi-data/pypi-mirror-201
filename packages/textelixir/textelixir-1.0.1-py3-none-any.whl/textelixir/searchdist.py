import pandas as pd
import plotly.express as px

class SearchDist:
    def __init__(self, conn, results, group_by, search_queries):
        self.conn = conn
        self.results = results
        self.group_by = group_by
        self.search_queries = search_queries
        self.dist = self.get_dist()


    def get_dist(self):
        dist = {}
        c = self.conn.cursor()
        # Get word ids from search results
        
        word_ids = [str(result[0]) if isinstance(result[0], int) else str(result[0][0]) for _, results in self.results.items() for result in results]
        joined_word_ids = ', '.join(word_ids)

        # Get actuals for the group_by column(s)
        c.execute(f"""
            SELECT {self.group_by}.value, COUNT({self.group_by}) 
            FROM corpus as c 
            JOIN {self.group_by} ON {self.group_by}.id = c.{self.group_by} 
            WHERE c.id IN ({joined_word_ids}) 
            GROUP BY {self.group_by}
            """)
        actuals = dict(c.fetchall())

        # Get totals for the group_by column
        c.execute(f"""
            SELECT {self.group_by}.value, COUNT({self.group_by}) 
            FROM corpus as c 
            JOIN {self.group_by} ON {self.group_by}.id = c.{self.group_by} 
            GROUP BY {self.group_by}
        """)
        totals = dict(c.fetchall())


        # Get unique for the group_by column
        c.execute(f"""
            SELECT {self.group_by}.value, COUNT(DISTINCT LOWER(w.word))
            FROM corpus as c
            JOIN {self.group_by} ON {self.group_by}.id = c.{self.group_by}
            JOIN word as w ON w.id = c.word
            WHERE c.id IN ({joined_word_ids})
            GROUP BY {self.group_by}
        """)
        uniques = dict(c.fetchall())

        # Combine dictionaries.
        for group, total in totals.items():
            dist[group] = {
                'freq': actuals[group] if group in actuals else 0,
                'total': total,
                'unique': uniques[group] if group in uniques else 0
            }
            dist[group]['freq/total'] = round(dist[group]['freq'] / dist[group]['total'], 4)
            dist[group]['unique/total'] = round(dist[group]['unique'] / dist[group]['total'], 4)
        
        ibrk = 0
        
        # Calculate other useful metrics.
        search_total = sum(v['freq'] for k, v in dist.items())
        corpus_total = sum(v['total'] for k, v in dist.items()) 
        for key, value in dist.items():
            # Add expected value
            percentage = value['total'] / corpus_total
            dist[key]['expected'] = round(percentage * search_total, 1)
            # Add frequency per million value
            dist[key]['freqPerMil'] = round(dist[key]['freq'] / dist[key]['total'] * 1000000, 2)
            
        return dist


    def make_chart(self, output_metric='freqPerMil', x_name=None, y_name=None, hide_zeros=False, chart_title=None, sort_x=None, sort_y=None, limit=0):
        x_name = x_name if x_name else self.group_by
        y_name = y_name if y_name else output_metric
        hide_zeros = hide_zeros if hide_zeros else False
        chart_title = chart_title if chart_title else f'Search Distribution for {", ".join(self.search_queries)}'
        sort_x = sort_x if sort_x else None
        sort_y = sort_y if sort_y else None
        limit = limit if limit > 0 else 0
        x = []
        y = []

        for k, v in self.dist.items():
            # Hide any values that have 0 in their frequency.
            if hide_zeros == True and v['freq'] == 0:
                continue
            x.append(k)
            y.append(v[output_metric])

        zipped_data = list(zip(x, y))
        # Check for any sorting to be done.
        if sort_x == 'ascending':
            zipped_data.sort(key = lambda x: x[0]) 
        elif sort_x == 'descending':
            zipped_data.sort(key = lambda x: x[0], reverse=True)
            ibrk = 0
        
        if sort_y == 'ascending':
            zipped_data.sort(key = lambda x: x[1])
        elif sort_y == 'descending':
            zipped_data.sort(key = lambda x: x[1], reverse=True)

        # Limit the list if the "limit" argument is more than 0
        if limit > 0:
            zipped_data = zipped_data[0:limit]

        df = pd.DataFrame(zipped_data, columns =[x_name, y_name])
        return px.bar(df, x=x_name, y=y_name, title=chart_title)


    def show_chart(self, filename='figure.html', output_metric='freqPerMil', x_name=None, y_name=None, hide_zeros=False, chart_title=None, sort_x=None, sort_y=None, limit=0):
        fig = self.make_chart(output_metric, x_name, y_name, hide_zeros, chart_title, sort_x, sort_y, limit)
        if not filename.endswith('.html'):
            filename += '.html'
        fig.write_html(filename, auto_open=True)


    def save_chart(self, filename, output_metric='freqPerMil', x_name=None, y_name=None, hide_zeros=False, chart_title=None, sort_x=None, sort_y=None, limit=0):
        fig = self.make_chart(output_metric, x_name, y_name, hide_zeros, chart_title, sort_x, sort_y, limit)
        fig.write_image(filename)

    def export_as_txt(self, filename, sort_column=None, sort_dir='descending'):
        # Check to see if filename is valid
        if not isinstance(filename, str):
            raise Exception(f'The value `{filename}` is not a string. Please use a string for the filename argument.')
        # Check to see if sort_column has any invalid values
        valid_sort_columns = ['freq', 'freqPerMil', 'unique', 'expected', 'total', 'freq/total', 'unique/total']
        if sort_column and sort_column not in valid_sort_columns:
            raise Exception(f'The value `{sort_column}` is not valid for the `sort_column` argument. Please use one of the following values instead: {", ".join(valid_sort_columns)}')
        # Check to see if sort_dir is valid
        if sort_dir not in ['ascending', 'descending']:
            raise Exception(f'The value `{sort_dir}` is not valid for the `sort_dir` argument. Please use \'ascending\' or \'descending\'.')
        
        if sort_column:
            sort_dir = True if sort_dir == 'descending' else False
            self.dist = dict(sorted(self.dist.items(), key=lambda x: x[1][sort_column], reverse=sort_dir))
        with open(filename, 'w', encoding='utf-8') as file_out:
            print(f'{self.group_by}\tfreq\tfreqPerMil\tunique\texpected\ttotal\tfreq/total\tunique/total', file=file_out)
            for key, value in self.dist.items():
                print(key, 
                      value['freq'], 
                      value['freqPerMil'], 
                      value['unique'], 
                      value['expected'], 
                      value['total'], 
                      value['freq/total'], 
                      value['unique/total'], 
                      sep='\t', 
                      file=file_out)