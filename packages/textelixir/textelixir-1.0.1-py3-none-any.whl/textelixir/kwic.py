from pkg_resources import resource_filename
import json
import re
import math

JSDIR = resource_filename('textelixir', 'js')
CSSDIR = resource_filename('textelixir', 'css')
IMGDIR = resource_filename('textelixir', 'img')
ICONDIR = resource_filename('textelixir', 'icon')

class KWIC:
    def __init__(self, search_window, affix_sep, group_by, before, after):
        self.search_window = search_window
        self.affix_sep = affix_sep
        self.group_by = group_by
        self.before = before
        self.after = after
        self.kwic_lines = self.get_kwic_lines()


    def get_kwic_lines(self):
        kwic_lines = []
        for _, words in self.search_window.items():
            kwic_line = ''
            for word in words:
                if self.affix_sep:
                    if 'hit1' in word and 'hit2' in word:
                        kwic_line += f'\t{word[self.group_by]}\t'
                    elif 'hit1' in word:
                        kwic_line += f'\t{word[self.group_by]}{word["suffix"]}'
                    elif 'hit2' in word:
                        kwic_line += f'{word["prefix"]}{word[self.group_by]}\t'
                    else:
                        kwic_line += f'{word["prefix"]}{word[self.group_by]}{word["suffix"]}'
                else:
                    if 'hit1' in word and 'hit2' in word:
                        kwic_line += f'\t{word[self.group_by]}\t'
                    elif 'hit1' in word:
                        kwic_line += f'\t{word[self.group_by]}'
                    elif 'hit2' in word:
                        kwic_line += f' {word[self.group_by]}\t'
                    else:
                        kwic_line += f' {word[self.group_by]}'
                kwic_line = re.sub(r'^ ', r'', kwic_line)
                kwic_line = re.sub(r' *\t *', r'\t', kwic_line)
                
            kwic_lines.append(kwic_line)
        return kwic_lines


    def reformat_kwic(self, kwic_lines):
        new_lines = []
        for line in kwic_lines:
            hit1_index = self.find(line, 'hit1')
            hit2_index = self.find(line, 'hit2')
            new_lines.append({
                'before': line[0:hit1_index],
                'hit': line[hit1_index:hit2_index+1],
                'after': line[hit2_index+1:]
                })
        return new_lines
    
    def reformat_collocate(self, collocates):
        # Get min and max of the sample
        samples = [math.log2(v['sample']) for k, v in collocates.collocates.items()]
        min_sample = min(samples)
        max_sample = max(samples)
        range = max_sample - min_sample
        
        collocate_strength = {}
        for k, v in collocates.collocates.items():
            sample = math.log2(v['sample']) - min_sample
            diff = round(abs(((range - sample) / (range / 10)) - 10), 1)
            collocate_strength[k] = diff if diff > 0.0 else 0.1
        return {collocates.group_by: collocate_strength}

    def find(self, arr, key):
        for i, dic in enumerate(arr):
            if key in dic:
                return i
        return -1


    def export_as_html(self, filename, collocates=None):
        if self.before > 10 or self.after > 10:
            print('WARNING: The HTML view of KWIC lines isn\'t designed well to display more than 10 words before or after a search term. TextElixir will still create the file because I don\'t believe in corpus analysis limitations.')
        kwic_lines = self.reformat_kwic(list(self.search_window.values()))
        if collocates:
            collocates = self.reformat_collocate(collocates)

        left_dots = ''.join([f'<span class="dot" data-order="l{i}"></span>' for i in range(0, self.before)])
        right_dots = ''.join([f'<span class="dot" data-order="r{i}"></span>' for i in range(0, self.after)])
        with open(filename, 'w', encoding='utf-8') as file_out:
            file_out.write(f"""<!DOCTYPE html>
    <html>
        <head>
        <title>KWIC Lines</title>
        <link href="{CSSDIR}/tippy.css"         rel="stylesheet"/>
        <link href="{CSSDIR}/bootstrap.min.css" rel="stylesheet" />
        <link href="{CSSDIR}/kwic.css"          rel="stylesheet" />
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">KWIC Lines</h1>
                <button class="btn btn-primary copyAll align-left" id="copyButton"><img class="ic" src="{ICONDIR}/clipboard.svg"> Copy All</button><button id="showAll" class="btn btn-primary align-right"><img class="ic" src="{ICONDIR}/cog.svg"> Table Options</button>
                <table class="table" id="table">
                    <thead>
                        <tr><td class="text-right">Before</td><td class="text-center">Hit</td><td colspan="2">After</td></tr>
                        <tr><td class="text-right">{left_dots}</td><td class="text-center"><span class="dot" data-order="c"></span></td><td colspan="2">{right_dots}</td></tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
            <script>
                let ICONDIR = '{ICONDIR}';
                let beforeWindow = {self.before};
                let afterWindow = {self.after};
                const data = {json.dumps(kwic_lines, ensure_ascii=False)};
                const collocates = {json.dumps(collocates, ensure_ascii=False) if collocates else '{}'};
            </script>
            <script src="{JSDIR}/kwic.js"></script>
            <script src="{JSDIR}/popper.js"></script>
            <script src="{JSDIR}/tippy.js"></script>
            <script src="{JSDIR}/tippys.js"></script>
            </body>
            </html>""")
