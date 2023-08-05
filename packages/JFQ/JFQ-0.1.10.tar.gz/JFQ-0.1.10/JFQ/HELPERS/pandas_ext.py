import datetime as _datetime
import openpyxl as _openpyxl
import pandas as _pd


#---------------------
# DF and dates manipulation
#---------------------

def normalise_df(df,base=100):
    normalised = df.copy()
    for col in normalised.columns:
        start_value = normalised[col][0]
        normalised[col]=normalised[col]*base/start_value
    return normalised

def excel_date(date1):
    temp = _datetime.date(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def parse_dates_quickly_strict(s, formato = '%Y-%m-%d'):
    """
    s is a time series in the form of DF['date column']
    If not specified, formato = YYYY-MM-DD format
    """
    dates = {date:_pd.to_datetime(date, format=formato) for date in s.unique()}
    return s.map(dates)

#---------------------
# EXCEL READ AUX FUNCTIONS ¦
#---------------------

def read_named_range_from_xlsx(xlsx_file, range_name, has_labels=True, first_col_index=False):
    """
    :param xlsx_file: Full drive path, using forward slash ("/") if needed
    :param range_name: can be a standard Excel reference ('Sheet1!A2:B7') or named region ('ADR')
    :param has_labels: True takes the first row as the column headers
    :param first_col_index:  True makes the first column as the index
    :return: panda df as per the above
    NOTE1: IT DOESN'T WORK OUT OF THE BOX FOR EXCEL TABLES - WE NEED TO DEFINE A NEW NAME
           OVERLAPPING THE TABLE WITH AN EXTRA ROW, SO THAT ITS DEFINITION IS IN THE FORM
           OF "SHEET1!$A3:B7" OR SIMILAR
    NOTE2: IT DOESN'T WORK WITH PASSWORD-PROTECTED BOOKS
    """

    # EXAMPLE CALL
    # from DB_functions_store_retrieve_data import read_named_range_from_xlsx
    #
    # df = read_named_range_from_xlsx(
    #     xlsx_file='C:/Users/juanf/Dropbox/_PROGRAMMING/BBG_python/SISTEMA/SISTEMA_OUTPUT/Book1JuanNP.xlsm',
    #     range_name='ADRs_named_range',
    #     has_labels=True,
    #     first_col_index=False)

    wb = _openpyxl.load_workbook(xlsx_file, data_only=True, read_only=True)
    if '!' in range_name:
        # passed a worksheet!cell reference
        ws_name, reg = range_name.split('!')
        if ws_name.startswith("'") and ws_name.endswith("'"):
            # optionally strip single quotes around sheet name
            ws_name = ws_name[1:-1]
        region = wb[ws_name][reg]
    else:
        # passed a named range; find the cells in the workbook
        full_range = wb.defined_names[range_name]
        if full_range is None:
            raise ValueError(
                'Range "{}" not found in workbook "{}".'.format(range_name, xlsx_file)
            )
        # convert to list (_openpyxl 2.3 returns a list but 2.4+ returns a generator)
        destinations = list(full_range.destinations)
        if len(destinations) > 1:
            raise ValueError(
                'Range "{}" in workbook "{}" contains more than one region.'
                .format(range_name, xlsx_file)
            )
        ws, reg = destinations[0]
        # convert to worksheet object (_openpyxl 2.3 returns a worksheet object
        # but 2.4+ returns the name of a worksheet)
        if isinstance(ws, str):
            ws = wb[ws]
        region = ws[reg]
    # headers and data
    if has_labels:
        cols = [cell.value for cell in region[0]]
        df = _pd.DataFrame(data=[[cell.value for cell in row] for row in region[1:]], columns=cols)
    else:
        df = _pd.DataFrame(data=[[cell.value for cell in row] for row in region[1:]])
    # index
    if first_col_index:
        df.set_index(df.columns[0], inplace=True)
    # return
    return df


def read_ADR_table(file_path='', range_name='',
                   selected_fields=['Source instrument', 'BBG', 'Price multiplier', 'Crncy', 'Crncy dividend', 'Type',
                                    'Cap gains treatment', 'Duration_Nominal', 'Duration', 'Duration_Yield']):
    """
    :param file_path: if we leave it as '', it will read from the clipboard; else put fullpath in there with forward slashes
    :param range_name: the specific range we're targetting in the spreadsheet
    :param selected_fields: the ones we need are already set by default
    :return: df with adr table, indexed by integers and showing the selected fields
    """

    if (file_path == '') or (range_name == ''):
        adr = _pd.read_clipboard(sep='\t', thousands=',')
    else:
        adr = read_named_range_from_xlsx(xlsx_file=file_path, range_name=range_name, has_labels=True,
                                         first_col_index=False)
    if len(selected_fields) > 0:
        adr = adr[selected_fields]
    adr.dropna(how='all', inplace=True)
    # engine = create_SQLalchemy_connection(dbFile=blotterDatabasePath)
    # adr.to_sql(name='adr_table', con=engine, index=False, if_exists='replace')
    # print('Done...saved in DB and results in adr')
    return adr

