import re
import unicodedata


def parse_text(string, tagger, lang, nlp):
    if tagger == None:
        return default_text_parser(string, lang)
    # TODO: Implement
    elif tagger.startswith('spacy'):
        return spacy_text_parser(string, nlp)


def default_text_parser(string, lang):
    string = re.sub(r'[“”]', r'"', string)
    string = re.sub(r'[’‘]', r"'", string)
    sentences = re.findall(r'\s*(.+?(?:[?!]+|$|\.(?=\s+[A-Z]|$)))\s*', string)
    split_sentences = []
    for sentence in sentences:
        search = re.search(re.escape(sentence), string)
        end = search.regs[0][1]

        if sentence.startswith('” '):
            if len(split_sentences) > 0:
                split_sentences[-1] += '” '
                split_sentences[-1] = split_sentences[-1].strip()
                split_sentences.append(sentence[2:].strip())
            else:
                split_sentences.append(sentence)

        elif re.search(r'^[A-Z][a-z]*\.$', sentence):
            if len(split_sentences) > 0:
                split_sentences[-1] += f' {sentence}'
            else:
                split_sentences.append(sentence)

        elif subsearch := re.search(r'^\([A-Z0-9][^\)]*\.\)', sentence):
            if len(split_sentences) > 0:
                split_sentences[-1] += ' ' + subsearch.group(0)
                split_sentences.append(sentence[subsearch.regs[0][1]:].strip())
            else:
                split_sentences.append(sentence)

        elif all([unicodedata.category(i).startswith('P') for i in sentence]):
            if len(split_sentences) > 0:
                split_sentences[-1] += sentence
            else:
                split_sentences.append(sentence)
        else:
            split_sentences.append(sentence.strip())
        string = string[end:]
    if final_string := string.strip() != '':
        split_sentences.append(final_string)
    return [default_word_split(s) for s in split_sentences]

def default_word_split(string):
    # First split the sentence by em-dashes, en-dashes, and ellipses. (Pending final list for English)
    sentence_blocks = re.split(r'[\(\)\[\]—…–]', string)
    # Collect all split words into this var.
    split_words = []
    # Collect any pending puncutation that should be a prefix in this var.
    pending_punct = ''
    # Iterate through each element of the sentence_blocks
    for block_index, s_block in enumerate(sentence_blocks):
        # If it's the second iteration or greater, add the first char into pending punctuation.
        # (This will be any of the punctuation from the beginning of the function.)
        if block_index > 0:
            pending_punct += string[0]
            string = string[1:]
        # Split the sentence block into words.
        words = re.findall(r'([!?,;:.&"-]+|\S*[A-Z]\.|\S*(?:[^!?,;:.\s&-]))', s_block)
        # Iterate through those words.
        for word in words:
            # Search for the word within the original string to get the begin and end indices.
            search = re.search(re.escape(word), string)
            begin = search.regs[0][0]
            end = search.regs[0][1]
            # Set the prefix to be '' if the search starts at the 0th index. This means there is no punctuation.
            # Otherwise, there is punctuation.
            prefix = '' if begin == 0 else string[0:begin]

            # Check to see if the word we have contains entirely punctuation or not.
            punct_check = all([unicodedata.category(i).startswith('P') for i in word])
            # If word we currently have is all punctuation, add it to the pending_punct to be added on the next word.
            if punct_check:
                pending_punct += f'{prefix}{word}'
            else:
                # If it's not, then we assume it's a word and then we can clear out the pending_punct by adding it to this word.
                if pending_punct != '':
                    prefix = pending_punct + prefix
                    pending_punct = ''
                split_words.append({'prefix': prefix, 'word': word})
            # Cut the original string to where the end of the word we found.
            string = string[end:]
    # Add any remaining punctuation as a suffix of the last word.
    if pending_punct != '':
        split_words[-1]['suffix'] = pending_punct
    return split_words

def spacy_text_parser(string, nlp):
    # Em dashes are generally not split properly.
    string = re.sub(r'([—«»])', r'  \1  ', string)
    # Contains sublists that contain dictionaries for each word.
    split_sentences = []
    # This list contains each start_char index to identify duplicates.
    start_chars = []

    current_read_index = 0
    start_char = 0
    doc = nlp(string)

    is_overflow_punct = False
    pending_punct = ''

    for sent_idx, sent in enumerate(doc.sents):
        split_sentences.append([])


        for word_idx, word in enumerate(sent):
            # Get the start char and end char of the string.
            start_char = string.index(word.text, start_char)
            if start_char not in start_chars:
                start_chars.append(start_char)
                duplicate = False
            else:
                duplicate = True
            end_char = start_char + len(word.text)
            actual_text = string[start_char:end_char]

            punct_check = all([unicodedata.category(i).startswith('P') or unicodedata.category(i).startswith('Zs') for i in actual_text])
            if punct_check or actual_text == ' ':
                pending_punct += string[current_read_index:start_char] + actual_text
                current_read_index = end_char
                start_char = end_char
                continue
            xpos = word.tag_
            pos = word.pos_
            lemma = word.lemma_.upper()

            if lemma == None:
                lemma = actual_text.upper()

            if duplicate:
                # continue
                split_sentences[-1][-1]['pos'] += f'-{pos}'
                split_sentences[-1][-1]['lemma'] = f'-{lemma}'
                split_sentences[-1][-1]['xpos'] = f'-{xpos}'
            else:
                if pending_punct != '':
                    prefix = pending_punct + string[current_read_index:start_char]
                    pending_punct = ''
                else:
                    prefix = string[current_read_index:start_char]
                split_sentences[-1].append({
                    'word': actual_text,
                    'xpos': xpos,
                    'pos': pos,
                    'lemma': lemma.upper(),
                    'prefix': prefix,
                })
            current_read_index = end_char
            start_char = end_char
        split_sentences = [s for s in split_sentences if s != []]
        if pending_punct != '':
            if split_sentences != [[]] and split_sentences != []:
                split_sentences[-1][-1]['suffix'] = pending_punct
                pending_punct = ''
        else:
            split_sentences[-1][-1]['suffix'] = ''
        # Add 2 spaces between paragraphs
        if len(split_sentences) > 0 and len(split_sentences[-1]) > 0:
            if not split_sentences[-1][0]['prefix'].startswith('  '):
                split_sentences[-1][0]['prefix'] = '  ' + split_sentences[-1][0]['prefix']
            if not split_sentences[-1][-1]['suffix'].endswith('  '):
                split_sentences[-1][-1]['suffix'] += '  '

        # ibrk = 0

    if len(string[start_char:]) != 0:
        if string[start_char:] == ' ':
            if len(split_sentences) == 0:
                split_sentences.append([{'prefix': string}])
            else:
                split_sentences[-1][-1]['suffix'] += ' '
        else:
            raise Exception('String is missing from data. The developer should be contacted in order to determine what is wrong.')
    # Add extra spaces at beginning and end of each sentence.
    
    return split_sentences