#!/usr/bin/env python3
#!-*- coding: utf-8 -*-

import os, re, json, yaml, msgpack

def list_files(dirpath, extension = None, recursively = False):
    ret = []
    pattern = re.compile('\.' + extension + '$') if extension else None
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        if os.path.isdir(filepath):
            if recursively:
                ret.extend(list_files(filepath, extension, recursively))
            else:
                continue
        elif pattern and not re.search(pattern, filename):
            continue
        else:
            ret.append(filepath)
    ret.sort()
    return ret


def create_file(filepath):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    f = open(filepath, 'w')
    f.close()
    return True

def read_file(filepath):
    with open(filepath, 'r') as f:
        ret = f.read()
    return ret

def write_file(content, filepath):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'w') as f:
        ret = f.write(content)
    return ret


def read_lines(filepath, comment_prefix=None):
    with open(filepath, 'r') as f:
        ret = [line.strip('\n\r') for line in f.readlines()]
    if comment_prefix:
        ret = list(filter(lambda x: not x.startswith(comment_prefix), ret))
    return ret

def write_lines(lines, filepath):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'w') as f:
        f.write("\n".join(lines))
    return True

def append_lines(lines, filepath):
    with open(filepath, 'a') as f:
        f.write('\n'.join(lines) + '\n')
    return True


def write_csv(records, filepath, col_names = None,
        delimiter='\t', has_header = True):

    if not col_names:
        col_names = []
    # pickup all columns
    for r in records:
        for k in r:
            if not k in col_names:
                col_names.append(k)

    create_file(filepath)
    if has_header:
        append_lines([delimiter.join(col_names)], filepath)

    for r in records:
        row = []
        for col in col_names:
            if col in r and r[col] is not None:
                row.append(_escape_string(str(r[col]), delimiter))
            else:
                row.append('')
        append_lines([delimiter.join(row)], filepath)
    return

def append_csv(records, filepath, delimiter='\t'):
    with open(filepath, 'r') as f:
        header_line = f.readline().strip('\n\r')
    col_names = header_line.split('\t')
    col_set = set(col_names)

    for r in records:
        row = []
        for col in col_names:
            if col in r and r[col] is not None:
                row.append(_escape_string(str(r[col]), delimiter))
            else:
                row.append('')
        for key in r:
            if not key in col_set:
                raise Exception('Invalid column {} found'.format(key))
        append_lines([delimiter.join(row)], filepath)
    return

def _escape_string(s, delimiter):
    s = s.replace(delimiter, ' ')
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    return s


def read_csv(filepath, delimiter='\t', has_header = True, comment_prefix = None):
    lines = read_lines(filepath, comment_prefix = comment_prefix)
    col_names = None
    if has_header:
        header = lines[0]
        col_names = header.split(delimiter)
        lines = lines[1:]
    ret = []
    for line in lines:
        cols = line.split(delimiter)
        if has_header and len(cols) != len(col_names):
            message = 'CSV format is invalid. ' + \
                      'There are %d columns in header, ' % (len(col_names)) + \
                      'but the following line has %d columns. \n' % len(cols) + \
                      '%s' % line
            raise Exception(message)
        tmp = None
        if has_header:
            tmp = {}
            for i in range(len(cols)):
                if cols[i]:
                    tmp[col_names[i]] = cols[i]
        else:
            tmp = cols
        ret.append(tmp)
    return ret


def read_json(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        ret = json.load(f)
    return ret

def write_json(content, filepath, indent=2):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'w', encoding='utf8') as f:
        json.dump(content, f, ensure_ascii=False, indent=indent)
    return True


def read_yaml(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        ret = yaml.load(f, Loader=yaml.FullLoader)
    return ret

def write_yaml(content, filepath, indent=2):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'w', encoding='utf8') as f:
        yaml.dump(content, f, indent=indent)
    return True

def read_msgpack(filepath):
    with open(filepath, 'rb') as f:
        ret = msgpack.unpackb(f.read())
    return ret


def write_msgpack(content, filepath):
    dirpath = os.path.dirname(filepath)
    if dirpath != '' and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        f.write(msgpack.packb(content))
    return True


