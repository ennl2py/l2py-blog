import re

def ch_content(content):
    ch_rule = re.compile(r'<[^>]+>', re.S)
    ch_content = ch_rule.sub('', content)
    return ch_content
