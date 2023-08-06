import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
class MATTR:
    def __init__(self, conn, window, step, filter, document):
        self.conn = conn
        self.window = window
        self.step = step
        self.filter = filter
        self.document = document
        self.mattr = self.get_mattr()
    
    def get_mattr(self):
        c = self.conn.cursor()

        mattr = [] if self.document == None else {}
        document_values = [1]
        # document_values = self.get_metadata_list(self.document)
        for value in document_values:
            # I need to do another join to get the correct document table!
            document_join_condition = '' if self.document == None else f'JOIN {self.document} as x ON x.id = c.{self.document}'
            where_condition = '' if self.document == None else f'WHERE x.value = "{value}"'
            c.execute(f"""
                SELECT LOWER(w.word) FROM corpus AS c 
                JOIN word AS w ON w.id = c.word
                {document_join_condition} 
                {where_condition};
                """)

            rows = c.fetchall()
        
            for i in range(0, len(rows)-self.window-1, self.step):
                tokens = self.window
                if tokens != self.window:
                    raise Exception('Window value is not equal to token value.')
                types = len(set(rows[i:i+self.window]))
                mattr.append(types / tokens)
        return mattr
            

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

    
    def show_chart(self, x_name, y_name, chart_title):
        x = []
        y = []

        for idx, ttr in enumerate(self.mattr):
            x.append(f'Words {idx+1}-{idx+1+self.window}')
            y.append(ttr)

        zipped_data = list(zip(x, y))

        df = pd.DataFrame(zipped_data, columns =[x_name, y_name])
        fig = px.line(df, x=x_name, y=y_name, title=chart_title)
        fig.show()


    def save_chart(self, filename, x_name, y_name, chart_title):
        x = []
        y = []

        for idx, ttr in enumerate(self.mattr):
            x.append(f'Words {idx+1}-{idx+1+self.window}')
            y.append(ttr)

        zipped_data = list(zip(x, y))

        df = pd.DataFrame(zipped_data, columns =[x_name, y_name])
        fig = px.line(df, x=x_name, y=y_name, title=chart_title)
        fig.write_image(filename)

    # def show_chart(self, x_name, y_name, chart_title):
    #     x = []
    #     y = []

    #     for idx, ttr in enumerate(self.mattr):
    #         x.append(f'Words {idx+1}-{idx+1+self.window}')
    #         y.append(ttr)

    #     x = np.array(x)
    #     y = np.array(y)
    #     fig = go.Figure()

    #     fig.add_trace(go.Scatter(x=x, y=y, name='spline', text=['test'], line_shape='spline'))
    #     fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    #     fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
    #     # df = pd.DataFrame(zipped_data, columns =[x_name, y_name])
    #     # fig = px.line(df, x=x_name, y=y_name, title=chart_title)
    #     fig.show()