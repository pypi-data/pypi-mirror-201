from optparse import OptionParser as _OptionParser
import pandas as _pd

#Reviewed aux functions:

def parseCmdLine():
    parser = _OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="localhost")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options



def groupOutput(listSecID,listFieldID,listFieldScale,oneTablePer,response,onlyCommonDates=True,fillna=False,fillna_method="ffill"):
    '''
    :param listSecID: as per the BDH definition
    :param listFieldID:  as per the BDH definition
    :param listFieldScale:  as per the BDH definition
    :param oneTablePer:  as per the BDH definition
    :param response:  as per the BDH output (a list of [  [securityname, df for that security] ] )
    :return: list of DFs each organised as requestd, by FIELD or by SECURITY
    '''
    fieldAndScale=list(zip(listFieldID,listFieldScale))
    groupedResponse = []


    if oneTablePer=="FIELD":
        # one table = one field, multiple securities
        for (field,scale) in fieldAndScale:
            # ******************************
            # organise list of relevant dates
            df = response[0][1][['date']].copy().set_index('date')  # date
            for response_item in response:
                if onlyCommonDates == True:
                    df.index = df.index.intersection(response_item[1][['date']].copy().set_index('date').index)
                else:
                    df.index = df.index.union(response_item[1][['date']].copy().set_index('date').index)
            df = df.sort_index(ascending=True)
            #******************************
            for security in response:
                sec_brief = security[1][['date', field]].copy().set_index('date')
                sec_brief = sec_brief.rename(columns={field: security[0]})
                #zzzzzzz if by joining the new frame we would get an empty frame, then don't do it
                if onlyCommonDates:
                    df_test=df.join(sec_brief, how='inner')
                else:
                    df_test = df.join(sec_brief, how='outer')
                if df_test.empty==False:
                    df=df_test
                    if fillna:
                        df = df.fillna(method=fillna_method)
                else:
                    print('empty frame alert')
                #zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            separator = ("" if scale == "" else "_")
            df.index.rename(field+separator+scale, True)
            groupedResponse.append(df)
        a = 0
        for (field,scale) in fieldAndScale:
            try:
                if scale == "REBASE100":
                    for securityName in listSecID:
                        baseValue = groupedResponse[a][securityName].dropna()[0]/100
                        groupedResponse[a].loc[:, securityName] /= baseValue
                if scale=="RETURNS":
                    groupedResponse[a]=groupedResponse[a].pct_change(1)
            except:
                print(f"cannot rebase {field}")
            a=a+1
    else:
        # one table = one security, multiple fields
        for security in response:  #this should provide them in the same order
            try:
                df = security[1].set_index('date')
                # ****new stuff****
                a=0
                for (field,scale) in fieldAndScale:
                    separator=("" if scale=="" else "_")
                    df.columns.values[a]=field+separator+scale
                    a=a+1
                #******************
                df.index.rename(security[0], True)
                if fillna:
                    df = df.fillna(method=fillna_method)
                groupedResponse.append(df)
            except:
                df = None
        a=0
        for table in groupedResponse:
            if isinstance(table, _pd.DataFrame):
                for (field,scale) in fieldAndScale:
                    separator=("" if scale=="" else "_")
                    if scale == "REBASE100":
                        groupedResponse[a].loc[:, field+separator+scale] /= (groupedResponse[a][field+separator+scale][0]/100)
                    if scale=="RETURNS":
                        groupedResponse[a][field+separator+scale]=groupedResponse[a][field+separator+scale].pct_change(1)
            a=a+1


    return groupedResponse

#---------------------
# TREE AUX FUNCTIONS ¦
#---------------------

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]







