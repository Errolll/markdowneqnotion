
def convert_inline_eq(plain_text): #For each richtext
    plain_text: str
    
    plain_text = plain_text.replace('<br>', '\n')
    
    # Find Eq Notain idx
    set_idx = [[]]
    for ch_idx, ch in enumerate(plain_text):
        
        if ch_idx != len(plain_text)-1 and len(set_idx[-1]) == 2:
            set_idx.append([])
            
        if ch == '$':
            set_idx[-1].append(ch_idx)
    
    rich_texts = []
    
    
    if not set_idx[-1]:
        set_idx.pop(-1)
        
    if not set_idx:
        _element = {
            'annotations': {
                'bold': False, 
                'italic': False, 
                'strikethrough': False, 
                'underline': False, 
                'code': False, 
                'color': 'default'
                },
            'href': None,
            'plain_text': plain_text,
            'text': {
                'content': plain_text,
                'link': None
                },
            'type': 'text'
            }
        rich_texts.append(_element)    
    
    if set_idx and len(set_idx[0]) == 2:
        # First non-inline equation
        if set_idx[0][0] != 0:
            _chunk = plain_text[0:set_idx[0][0]]
    
            _element = {
                'annotations': {
                    'bold': False, 
                    'italic': False, 
                    'strikethrough': False, 
                    'underline': False, 
                    'code': False, 
                    'color': 'default'
                    },
                'href': None,
                'plain_text': _chunk,
                'text': {'content': _chunk,
                         'link': None
                        },
                'type': 'text'
                }
            rich_texts.append(_element)

        # Start from first inline equation
        for s_i ,s in enumerate(set_idx):
            # '$ ...'
            
            # Equation
            eq_start = s[0]+1
            eq_end = s[-1]
            
            _chunk_eq = plain_text[eq_start:eq_end]
            
            _element = {
                'annotations': {
                    'bold': False, 
                    'italic': False, 
                    'strikethrough': False, 
                    'underline': False, 
                    'code': False, 
                    'color': 'default'
                    },
                'href': None,
                'plain_text': _chunk_eq,
                'equation': {
                    'expression': _chunk_eq
                    },
                'type': 'equation'
                }
            rich_texts.append(_element)
            
            # Non Equation
            neq_start = eq_end+1
            if s_i == len(set_idx)-1:
                if eq_end == len(plain_text)-1:
                    continue
                else:
                    neq_end = None
            elif not set_idx[s_i+1]:
                continue
            else:            
                neq_end = set_idx[s_i+1][0]
            
            _chunk_neq = plain_text[neq_start:neq_end]
            
            _element = {
                'annotations': {
                    'bold': False, 
                    'italic': False, 
                    'strikethrough': False, 
                    'underline': False, 
                    'code': False, 
                    'color': 'default'
                    },
                'href': None,
                'plain_text': _chunk_neq,
                'text': {
                    'content': _chunk_neq,
                    'link': None
                    },
                'type': 'text'
                }
            rich_texts.append(_element)

    return rich_texts

def convert_eq(block, rich_texts): #or texts
    # rich_texts: list, rich text in a block
    update_value = {}
    
    # Math Block
    if rich_texts[0]['plain_text'].startswith('$$'):
        # math block
        
        exp_matheq = ''
        
        for _idx, _rich_text in enumerate(rich_texts):
            if _idx == 0 or _idx == len(rich_texts)-1:
                exp_matheq += _rich_text['plain_text'].replace('$$','')
            else:
                exp_matheq += '_' + _rich_text['plain_text']
        
        # if exp_matheq.startswith('\n'):
        #     exp_matheq = exp_matheq[2:]
        # if exp_matheq.endswith('\n'):
            # exp_matheq = exp_matheq[:-1]

        _element = {
            'annotations': {
                'bold': False, 
                'italic': False, 
                'strikethrough': False, 
                'underline': False, 
                'code': False, 
                'color': 'default'
                },
            'href': None,
            'plain_text': exp_matheq,
            'equation': {
                'expression': exp_matheq
                },
            'type': 'equation'
            }            
        

        update_value = {'rich_text': [_element]}
        
        
    # Inline Equation
    else:
        # inline eq
        text_inlineeq = ''
        
        _plain_text = ''
        for _idx, _rich_text in enumerate(rich_texts):
            if len(_plain_text) > 0 :
                text_inlineeq += '_'
            _plain_text = _rich_text['plain_text']
            text_inlineeq += _plain_text
        
        _rich_texts = convert_inline_eq(text_inlineeq)

        update_value = {'rich_text': _rich_texts}

    return update_value
