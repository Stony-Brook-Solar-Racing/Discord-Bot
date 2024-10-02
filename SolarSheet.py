# DO NOT TOUCH # SET UP # DO NOT TOUCH # SET UP # DO NOT TOUCH
# DO NOT TOUCH # SET UP # DO NOT TOUCH # SET UP # DO NOT TOUCH
import gspread
import json

with open("config.json") as file:
    config = json.load(file)
credentials = config["gspread_creds"]

# gc = gspread.service_account('credentials/attendance-401819-cc26d3c62729.json')
gc = gspread.service_account_from_dict(credentials)
sheets = gc.open("attendance swiper")
worksheet = sheets.sheet1
record_sheet = sheets.get_worksheet(1)

# DO NOT TOUCH # SET UP # DO NOT TOUCH # SET UP # DO NOT TOUCH
# DO NOT TOUCH # SET UP # DO NOT TOUCH # SET UP # DO NOT TOUCH

# Add an entry to spreadsheet
# inout: true if in, false if out
def addEntry(name: str, time: str, inout: bool, cell: int, timeSpent: str):
    cell+=1
    worksheet.update_cell(2,1,cell)

    worksheet.update_cell(cell, 1, name)
    worksheet.update_cell(cell, 2, time)
    worksheet.update_cell(cell, 3, inout)
    worksheet.update_cell(cell, 4, timeSpent)
    # worksheet.update_cell(cell, 5, sessionNum)

def getNameAtRow(row):
    return worksheet.acell('A'+str(row))

def getTimeAtRow(row):
    return worksheet.acell('B'+str(row))

def getInOutAtRow(row):
    return worksheet.acell('C'+str(row))

def getSessionNum(row):
    return worksheet.acell('E'+str(row))

def getCounter():
    return int(worksheet.acell('A2').value)

SHOP_COUNT_CELL = "A2"
SHOP_ROWS_OFFSET = 2

def get_shop_ppl_count() -> int:
    return int(record_sheet.acell(SHOP_COUNT_CELL).value)

def update_shop_ppl_count(new_count: int):
    record_sheet.update_acell(SHOP_COUNT_CELL, new_count)

def get_ppl_in_shop_names() -> list[str]:
    count = get_shop_ppl_count()
    if count == 0:
        return []
    
    return record_sheet.get_values(f"A3:B{SHOP_ROWS_OFFSET + count}")[0]

"""
    Sheet2 Formatting
    Cols: A | B
        Name|Time In 
"""
def get_ppl_in_shop() -> list[list[str]]:
    count = get_shop_ppl_count()

    if count == 0:
        return [[]]
    row_start = SHOP_ROWS_OFFSET + count
    rows = record_sheet.batch_get(
        [f'A3:B{row_start}']
    )
    
    return rows[0]
    
def shop_add_person(full_name: str, time: str):
    count = get_shop_ppl_count()
    record_sheet.insert_row([full_name, time], get_shop_ppl_count() + SHOP_ROWS_OFFSET + 1 )
    update_shop_ppl_count(count + 1)

def shop_remove_person(full_name: str = None, index=None):
    ppl = get_ppl_in_shop()
    
    if len(ppl) == 0:
        print('Cannot remove person from empty list')
        return
    
    row_i = SHOP_ROWS_OFFSET + 1

    # if index is specified
    if index is not None:
        record_sheet.delete_rows(row_i + index)
        update_shop_ppl_count(get_shop_ppl_count() - 1) 

    # otherwise use the name to find row
    elif full_name is not None:
        matches = [i for i, row in enumerate(ppl) if row[0] == full_name]
        
        if len(matches) == 0:
            print('Name does not exists in the list')
            return None
        
        init_time = ppl[matches[0]][1]
        record_sheet.delete_rows(row_i + matches[0])
        update_shop_ppl_count(get_shop_ppl_count() - 1) 
        return init_time
    else:
        raise Exception("Neither full_name or index parameters were given")

