import os


def read_txt(infile, delimeter=None, maxsplit=-1, remove_newline=True, cols=None, line_limit=None):
    """read text file
    Args:
        infile: input file path
        delimiter
        maxsplit
        remove_newline
        cols: list of index
        num: number of lines that returned
    """

    if cols is not None and type(cols) != list and type(cols) == int:
        raise RuntimeError('cols must be a list or integer')
    if not os.path.exists(infile):
        raise RuntimeError('file not existed: {}'.format(infile))

    content = []
    for l in open(infile, 'r', encoding='utf8'):
        if line_limit is not None and len(content) >= line_limit:
            break
        if remove_newline:
            l = l.rstrip('\n')
        if delimeter is not None:
            l = l.split(delimeter, maxsplit=maxsplit)
            if cols is not None:
                if type(cols) == list:
                    l = [l[index] for index in cols]
                else:  # integer
                    l = l[cols]
        content.append(l)
    return content


def load_txt(infile, delimeter='\t', maxsplit=-1, batch_size=10000, remove_newline=True, cols=None):
    """load text file
    """

    chunk = []
    for l in open(infile, 'r', encoding='utf8'):
        if remove_newline:
            l = l.rstrip('\n')
        if delimeter is not None:
            l = l.split(delimeter, maxsplit=maxsplit)
            if cols is not None:
                if type(cols) == list:
                    l = [l[index] for index in cols]
                else:  # integer
                    l = l[cols]
        chunk.append(l)
        if len(chunk) >= batch_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
