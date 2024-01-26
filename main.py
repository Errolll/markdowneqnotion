import os
from notion_client import Client
from functions import convert_eq, convert_to_equation

if __name__ == '__main__':
    
    # ex: os.environ["NOTION_TOKEN"] = "secret_***"
    os.environ["NOTION_TOKEN"] = "<YOUR NOTION TOKEN>"
    
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    
    page_id = '<YOUR PAGE ID>'
    
    
    _blocks = list()
    
    has_more = True
    
    cursor_id = None
    while has_more:
    
        if cursor_id is not None:
            _block = notion.blocks.children.list(block_id=page_id, start_cursor=cursor_id)
        else:
            _block = notion.blocks.children.list(block_id=page_id)

        cursor_id = _block['next_cursor']
    
    
        if _block:
            _blocks.append(_block)
            has_more = _block['has_more']
    
            print(has_more)
        else:
            has_more = False
    
    blocks = dict().fromkeys(_block.keys())
    
    for _key in blocks:
        blocks[_key] = []
        for _block in _blocks:
            if hasattr(_block[_key], '__iter__'):
                blocks[_key].extend(_block[_key])
            else:
                blocks[_key].append(_block[_key])    
    
    update_values = []
    idx = 0
    
    blocks_table = []
    
    # First Convert Equations in the paragraph blocks (inline, math_block)
    for block in blocks['results']:
        
        block_type = block['type']
    
        if block_type == 'table':
            blocks_table.append(block)    
        elif 'rich_text' in block[block_type]:
            rich_texts = block[block_type]['rich_text']
            
            is_pass = False
            
            # Block Check
            if not rich_texts:
                is_pass = True
            else:
                for idx in range(len(rich_texts)):
                    if rich_texts[idx]['type']!='text':
                        is_pass = True
                        break
                    elif len(rich_texts[idx]['text']['content'])>2000:
                        is_pass = True
                        break
            if is_pass:
                continue
            
            update_values = {
                block_type: convert_eq(block, rich_texts)
                }
            
            try:
                notion.blocks.update(block_id=block['id'], **update_values)
            except:
                continue
        
    
    # Next, Convert Equations in the table blocks
    for block_table in blocks_table:
        rows_in_block = notion.blocks.children.list(block_table['id'])['results']
        update_value = {'table_row': {'cells': []}}
    
        for row_in_block in rows_in_block:
            cells_ = row_in_block['table_row']['cells'].copy()
            for cell_idx, cell in enumerate(cells_):
                plaintext_in_cell = ''
                for sublock_in_cell in cell:
                    if len(plaintext_in_cell) > 0 :
                        plaintext_in_cell += '_'                
                    plaintext_in_cell += sublock_in_cell['plain_text']
    
                cells_[cell_idx] = convert_to_equation(plaintext_in_cell)
            
            update_value['table_row']['cells'] = cells_
            
            notion.blocks.update(block_id=row_in_block['id'], **update_value)
            
        
    

        
