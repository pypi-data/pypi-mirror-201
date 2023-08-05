from __future__ import print_function
from __future__ import absolute_import
import blpapi as _blpapi
import pandas as _pd
import datetime as _datetime
from ..HELPERS import misc as _misc
from ..HELPERS import pandas_ext as _pandas_ext
import numpy as _np

#FULLY REVIEWED:
#BDH
#BDH_Disjoint
#BEQS
#BDP_One_Field --> improved to show field name in the index, and the ability to display securities as columns or as rows
#BDP_Multiple_Fields
#BDP_Dividends
#BDP_Bond_Cashflows -> improved to be able to specify face amount. Consider in the future simplifying the override structure to a settlement date parameter
#generate_universe -> improved and merged so that it returns both the universe as well as the unit and raw weights


def BDH(listSecID,listFieldID,listFieldScale,startDateYYYYMMDD,endDateYYYYMMDD,periodicityAdjustment="ACTUAL",periodicitySelection="DAILY",maxDataPoints=0,listOverrides = [],convertDatesToNumbers=False,oneTablePer="SECURITY",onlyCommonDates=True,return_as_dict=False,fillna=False,fillna_method="ffill"):
    '''
    Calls the historic data download function from bloomberg
    :param listSecID: list of the tickers we want to use, eg ["IBM US Equity", "AAPL US Equity"]
    :param listFieldID: list of the historical fields requested, eg ["PX_LAST"]
    :param listFieldScale: list matching the listFieldID length where each of the items is "RAW", "REBASE100", or "RETURNS". If left as an empty list, it will assume RAW.
    :param startDateYYYYMMDD: text string in YYYYMMDD format, eg "20061230"
    :param endDateYYYYMMDD: text string in YYYYMMDD format, eg "20061230"
    :param periodicityAdjustment: "ACTUAL","CALENDAR", or "FISCAL"
    :param periodicitySelection: "DAILY", "WEEKLY", "MONTHLY","QUARTERLY","SEMI_ANNUALLY","YEARLY"
    :param maxDataPoints: if 0, then no limitation
    :param overrides = list of overrides, where each override itself is a 2-uple of (override field,override value)
    :param convertDatesToNumbers: the default is False; if True, it converts it into a excel number equivalent
    :param oneTablePer: "SECURITY" (default: each table is one security, shows all fields) or "FIELD" (each table is one field, shows result for all securities)
    :param onlyCommonDates: If True, it will restrict df output to dates found in all
    :param return_as_dict: If true, the return will be a dictionary of the form field: table by field or security: table by security
    :param fillna: if True, fillna with fillna_method
    :param fillna_method: "ffill", etc
    :return: returns a list of data_frames (or dictionary, if return_as_dict is True) - if "SECURITY" has been chosen, then it'll be all fields for a given security; otherwise it'll be all securities for a given field.
    '''
    options = _misc.parseCmdLine()

    #if listFieldScale is an empty list
    if listFieldScale==[]:
        listFieldScale=[""]*len(listFieldID)

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("HistoricalDataRequest")

        # Fill the request
        #   a) securities
        for sec_id in listSecID:
            request.getElement("securities").appendValue(sec_id)
        #   b) fields
        for field_id in listFieldID:
            request.getElement("fields").appendValue(field_id)
        #   c) periodicity
        request.set("periodicityAdjustment", periodicityAdjustment)
        request.set("periodicitySelection", periodicitySelection)
        #   d) start and end date
        request.set("startDate", startDateYYYYMMDD)
        request.set("endDate", endDateYYYYMMDD)
        #   e) max data points
        request.set("maxDataPoints", maxDataPoints)
        #   f) other overrides
        if len(listOverrides)>0:
            overrides = request.getElement("overrides")
            for pair in listOverrides:
                override = overrides.appendElement()
                override.setElement('fieldId', pair[0])
                override.setElement('value', pair[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            print("Historical Request - "+str(listFieldID)+" - "+startDateYYYYMMDD+" : "+endDateYYYYMMDD)
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE
        allSecurities = []  #list of "securities". Each security is in the form of [sec_name, panda_dataframe with dates and fields]
        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    sd = msg.getElement("securityData")
                    sn = sd.getElement("security").getValue()
                    fd = sd.getElement("fieldData")
                    numDataRows=fd.numValues()
                    try:
                        labels=['date']+listFieldID
                        securityData=[]    #This variable will contain all data rows
                        for a in range(0,numDataRows):#each a "row of data", bbg calls them "fields"
                            dataRow=fd.getValue(a)
                            oneRow = [_np.nan]*len(labels)
                            numFields = dataRow.numElements()
                            for b in range(0,numFields):
                                v=dataRow.getElement(b).getValue(0)
                                if type(v) is _datetime.date and convertDatesToNumbers:
                                    v= _pandas_ext.excel_date(v)
                                # oneRow.append(v)
                                n = str(dataRow.getElement(b).name())
                                if n in labels:
                                    oneRow[labels.index(n)]=v
                            securityData.append(oneRow)
                            #print(row_list)
                        df= _pd.DataFrame.from_records(securityData, columns=labels)
                        # df.set_index('date')
                        #2023-02 force date to be a date
                        if not(convertDatesToNumbers):
                            df["date"]= _pd.to_datetime(df["date"])

                        #---------------------------------
                        if onlyCommonDates:
                            df=df.dropna()

                        oneSecurity=[sn,df]
                        allSecurities.append(oneSecurity)
                    except:
                        print('Empty values for '+sn+' on '+startDateYYYYMMDD+' - '+endDateYYYYMMDD)

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # at this point allSecurities = [[sec_name, panda_dataframe]], where panda_dataframe is of the format 'date','field 1'...'field n', for a given security

        #sort by listSecID
        sec_df_dict = {sec[0]: sec[1] for sec in allSecurities}
        allSecurities = [ [security,sec_df_dict[security]] if security in sec_df_dict else [security,None] for security in listSecID ]

        # group output and return values
        allSecuritiesGrouped= _misc.groupOutput(listSecID,listFieldID,listFieldScale,oneTablePer,allSecurities,onlyCommonDates,fillna,fillna_method)

        #if return as dict:
        if return_as_dict:
            allSecuritiesGrouped = {table.index.name:table for table in allSecuritiesGrouped}

        return allSecuritiesGrouped

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------


def BDH_Disjoint(listSecID,listFieldID,startDateYYYYMMDD,endDateYYYYMMDD,periodicityAdjustment="ACTUAL",periodicitySelection="DAILY",listOverrides = [],maxDataPoints=0,return_as_dict=False):
    allSecurities = BDH(listSecID=listSecID,
                        listFieldID=listFieldID,
                        listFieldScale=[],
                        startDateYYYYMMDD=startDateYYYYMMDD,
                        endDateYYYYMMDD=endDateYYYYMMDD,
                        periodicityAdjustment=periodicityAdjustment,
                        periodicitySelection=periodicitySelection,
                        maxDataPoints=maxDataPoints,
                        listOverrides=listOverrides,
                        oneTablePer="SECURITY",
                        onlyCommonDates=False,
                        return_as_dict=return_as_dict
                        )
    return allSecurities

def BDH_stacked(listSecID,listFieldID,startDateYYYYMMDD,endDateYYYYMMDD,periodicityAdjustment="ACTUAL",periodicitySelection="DAILY",listOverrides = [],maxDataPoints=0,stacked=True,index_reset=True):
    '''
    :param listSecID: as usual
    :param listFieldID: as usual
    :param startDateYYYYMMDD: as usual
    :param endDateYYYYMMDD: as usual
    :param periodicityAdjustment: as usual, can be ommited in most cases
    :param periodicitySelection: as usual, can be ommited in most cases
    :param listOverrides: as usual, can be ommited in most cases
    :param maxDataPoints: as usual, can be ommited in most cases
    :param stacked: If True (default) --> produces plotly-friendly data sets
    :param index_reset: If True (default) --> produces plotly-friendly data sets, otherwise the index will be (security,date)
    :return: plotly-friendly dataframe
    '''
    response = BDH_Disjoint(listSecID=listSecID, listFieldID=listFieldID, startDateYYYYMMDD=startDateYYYYMMDD, endDateYYYYMMDD=endDateYYYYMMDD, periodicityAdjustment=periodicityAdjustment, periodicitySelection=periodicitySelection, listOverrides=listOverrides,maxDataPoints=maxDataPoints,return_as_dict=False)
    allSecurities=_pd.DataFrame(columns=['security','date',listFieldID[0]],data=None)
    allSecurities.set_index(['security', 'date'], inplace=True)

    for sec in response:
        sec_name=sec.index.name
        sec.index.name='date'
        sec['security']=sec_name
        sec = sec.reset_index().set_index(['security', 'date'])
        allSecurities = _pd.concat([allSecurities,sec],axis=0)

    if stacked==False:
        allSecurities=allSecurities.unstack('security')

    if index_reset:
        allSecurities=allSecurities.reset_index()
    #return array
    return allSecurities

def BEQS(screenName,screenType,asOfYYYYMMDD):
    '''
    :param screenName: name of the pre-saved bloomberg screen
    :param screenType: normally this will be "PRIVATE"
    :param asOfYYYYMMDD: date as of which we want the screen
    :return: returns a list of tickers that meet the screen filters as of that date; no other fields returned
    '''

    session= _blpapi.Session()
    session.start()
    session.openService("//blp/refdata")

    refDataService=session.getService("//blp/refdata")
    request=refDataService.createRequest("BeqsRequest")
    request.set("screenName", screenName)
    request.set("screenType", screenType)
    overrides=request.getElement("overrides")
    override=overrides.appendElement()
    override.setElement('fieldId','PiTDate')
    override.setElement('value' ,asOfYYYYMMDD)
    override = overrides.appendElement()

    session.sendRequest(request)

    endReached = False
    while endReached == False:
        ev = session.nextEvent()
        if ev.eventType() == _blpapi.Event.RESPONSE or ev.eventType() == _blpapi.Event.PARTIAL_RESPONSE:
            for msg in ev:
                dt=msg.getElement("data").getElement("securityData")
                numSecurities=dt.numValues()
                tickers=[]
                for i in range(0,numSecurities):
                    sd=dt.getValue(i)
                    sn = sd.getElement("security").getValue()
                    fd = sd.getElement("fieldData") #we won't do anything with this since we only need the security name
                    tickers.append(sn+" Equity")
        if ev.eventType() == _blpapi.Event.RESPONSE:
            endReached = True
    print('EQS done for '+asOfYYYYMMDD+'!')
    return tickers

    # This is the info returned by default on an EQS - we ignore all but the ticker, we will request the info we need separately via BDH
    #Ticker = "OVAS US"
    #Short Name = "OVASCIENCE INC"
    #Market
    #Cap = 47430628.000000
    #Price: D - 1 = 1.330000
    #Total Return YTD = -13.071891
    #Revenue T12M = 570000.000000
    #EPS T12M = -2.220000

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def BDP_One_Field(listSecID,targetFieldName,overrideList,as_columns=True):
    '''
    Calls for one (1) field ref data request (including Total Return), can use multiple securities
    :param listSecID: list of the tickers we want to use, eg ["IBM US Equity", "AAPL US Equity"]
    :param targetFieldName: the field we're looking for (eg "CUST_TRR_RETURN_HOLDING_PER")
    :param overrideList: [[overrideParam,overrideValue]] eg [['CUST_TRR_START_DT',startDateYYYYMMDD],['CUST_TRR_END_DT',endDateYYYYMMDD]]
    :param as_columns: if True, securities will be in the columns field. Otherwise in the rows field.
    :return: returns a dataframe with {securities as column or row headers} and {one row or column with the data for ONE field as requested}
    '''
    options = _misc.parseCmdLine()

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("ReferenceDataRequest")

        # Fill the request
        #   a) securities
        for sec_id in listSecID:
            request.getElement("securities").appendValue(sec_id)
        #   b) fields
        request.getElement("fields").appendValue(targetFieldName)
        #   d) overrides
        overrides = request.getElement("overrides")
        for ovr in overrideList:
            override = overrides.appendElement()
            override.setElement('fieldId', ovr[0])
            override.setElement('value', ovr[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            if len(overrideList)>0:
                print("Processing BDP - "+targetFieldName+' - '+str(overrideList[0]))
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE
        tickers=[]
        fieldValues=[]

        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    dt = msg.getElement("securityData")
                    numSecurities = dt.numValues()
                    for i in range(0, numSecurities):
                        sd = dt.getValue(i)
                        sn = sd.getElement("security").getValue()
                        tickers.append(sn)
                        fd = sd.getElement("fieldData")
                        try:
                            field = fd.getElement(0)
                            field_value=field.getValue(0)
                            fieldValues.append(field_value)
                        except:
                            fieldValues.append(None)

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # return values
        output= _pd.DataFrame.from_records(data=[fieldValues], columns=tickers, index=[targetFieldName])
        if as_columns==False:
            output = output.transpose()

        return output

def BDP_Multiple_Fields(listSecID,listFields,overrideList):
    '''
    Generic reference data request (M securities, N fields). The code works even if there are "bad securities" :keyword "bad fields" (will output as None for those)
    :param listSecID: list of the tickers we want to use, eg ["IBM US Equity", "AAPL US Equity"]
    :param listFields: list of the tickers (eg ["NAME","CUST_TRR_RETURN_HOLDING_PER"])
    :param overrideList: [[overrideParam,overrideValue]] eg [['CUST_TRR_START_DT',startDateYYYYMMDD],['CUST_TRR_END_DT',endDateYYYYMMDD]]
    :return: returns a dataframe with {securities as rows} and {Fields as columns}
    '''
    options = _misc.parseCmdLine()

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    #initialise some counters for stats
    numFieldsEmptyValues = [0] * len(listFields)
    emptyTickers=[]

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("ReferenceDataRequest")

        # Fill the request
        #   a) securities
        for sec_id in listSecID:
            request.getElement("securities").appendValue(sec_id)
        #   b) fields
        for field_id in listFields:
            request.getElement("fields").appendValue(field_id)
        #   d) overrides
        overrides = request.getElement("overrides")
        for ovr in overrideList:
            override = overrides.appendElement()
            override.setElement('fieldId', ovr[0])
            override.setElement('value', ovr[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            if len(overrideList)>0:
                print("Processing BDP: "+str(len(listSecID))+' securities, '+str(len(listFields))+' fields and '+str(len(overrideList))+' overrides')
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE
        tickers=[]

        securityData=[]
        position = dict(zip(listFields, range(len(listFields))))
        emptyOneSecurity=[None]*len(listFields)

        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    dt = msg.getElement("securityData")
                    numSecurities = dt.numValues()
                    for i in range(0, numSecurities):
                        sd = dt.getValue(i)
                        sn = sd.getElement("security").getValue()
                        tickers.append(sn)
                        fd = sd.getElement("fieldData")
                        fieldValuesOneSecurity = list(emptyOneSecurity)
                        try:
                            numFields=fd.numElements()
                            for j in range(0,numFields):
                                field = fd.getElement(j)
                                field_value=field.getValue(0)
                                field_name=str(field.name())
                                fieldValuesOneSecurity[position[field_name]]=field_value
                            securityData.append(fieldValuesOneSecurity)
                            #record securities with no info
                            if fieldValuesOneSecurity==emptyOneSecurity:
                                emptyTickers.append(sn)
                            else:
                                # record number of empty fields for a valid security
                                for i in range(0, numFields):
                                    if fieldValuesOneSecurity[i] == None:
                                        numFieldsEmptyValues[i] += 1
                        except:
                            securityData.append(emptyOneSecurity)
                            emptyTickers.append(sn)

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # return values
        output = _pd.DataFrame.from_records(data=securityData, columns=listFields)
        output['security'] = tickers
        output.set_index('security', inplace=True)

        # print stats
        X_Header=True
        if len(emptyTickers)>0:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            print('WARNING: '+str(len(emptyTickers))+' BAD securities:')
            print(emptyTickers)
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            X_Header=False

        for i in range(0,len(listFields)):
            if numFieldsEmptyValues[i]>0:
                if X_Header:
                    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                    X_Header=False
                print('WARNING: Num empty '+listFields[i]+' in good securities = '+str(numFieldsEmptyValues[i]))
                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        return output



def BDP_Dividends(listSecID,overrideList):
    '''
    :param listSecID: list of the tickers we want to use, eg ["IBM US Equity", "AAPL US Equity"]
    :param overrideList: [[overrideParam,overrideValue]] eg [['DVD_START_DT',startDateYYYYMMDD],['DVD_END_DT',endDateYYYYMMDD]]  IF EMPTY -> GETS ALL DIVS
    :return: returns a dataframe with dividends paid by each ticker, each row includes the 7 fields pertaining to dividends
    '''
    dividendFields = ['Declared Date', 'Ex-Date', 'Record Date', 'Payable Date', 'Dividend Amount',
                      'Dividend Frequency', 'Dividend Type']
    targetFieldName='DVD_HIST_ALL'
    dataLineTemplate = _pd.DataFrame(index=[None], columns= (['ticker'] + dividendFields), data=None)
    allDividends = dataLineTemplate.copy()
    options = _misc.parseCmdLine()

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("ReferenceDataRequest")

        # Fill the request
        #   a) securities
        for sec_id in listSecID:
            request.getElement("securities").appendValue(sec_id)
        #   b) fields
        request.getElement("fields").appendValue(targetFieldName)
        #   d) overrides
        overrides = request.getElement("overrides")
        for ovr in overrideList:
            override = overrides.appendElement()
            override.setElement('fieldId', ovr[0])
            override.setElement('value', ovr[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            if len(overrideList)>0:
                print("Processing BDP - "+targetFieldName+' - '+str(overrideList[0]))
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE

        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    dt = msg.getElement("securityData")
                    numSecurities = dt.numValues()
                    for i in range(0, numSecurities):
                        sd = dt.getValue(i)
                        sn = sd.getElement("security").getValue()
                        fd = sd.getElement("fieldData")
                        try:
                            field = fd.getElement(0)
                            numDividendInstances = field.numValues()
                            for k in range(0,numDividendInstances):
                                dataLine=dataLineTemplate.copy()
                                dataLine['ticker']=sn
                                field_value=field.getValue(k)
                                for dividendField in dividendFields:
                                    try:
                                        dataLine[dividendField] = field_value.getElement(dividendField).getValue(0)
                                    except:
                                        dataLine[dividendField] = None
                                allDividends = allDividends.append(dataLine,ignore_index=True)
                        except:
                            print('Exception happened')
                            pass

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # clean the first row and return values
        allDividends=allDividends.dropna(how='all')
        allDividends['Dividend Amount'] = allDividends['Dividend Amount'].round(decimals=10)
        return allDividends


def BDP_Bond_Cashflows(listSecID,overrideList,face_amount=1):
    '''
    :param listSecID: list of the tickers we want to use, eg ["US912810SM18 Govt"] (note that the format " TII 0 1/4 02/15/50 Govt" doesn't work
    :param overrideList: [['SETTLE_DT', YYYYMMDD]] - If not specified it will be from today
    :param face_amount: if unspecified, it will return the cashflows per unit (eg 1 = 100%), otherwise specify eg 1,000,000
    :return: returns a dataframe with coupon and principal amounts paid from the settle date per unit ($1 of face value) or as otherwise specified by each ticker
    '''
    dividendFields = ['Payment Date', 'Coupon Amount', 'Principal Amount']
    targetFieldName='DES_CASH_FLOW'
    cfMultiplier = 1/1000000 * face_amount
    dataLineTemplate = _pd.DataFrame(index=[None], columns= (['ticker'] + dividendFields), data=None)
    allDividends = dataLineTemplate.copy()
    options = _misc.parseCmdLine()

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("ReferenceDataRequest")

        # Fill the request
        #   a) securities
        for sec_id in listSecID:
            request.getElement("securities").appendValue(sec_id)
        #   b) fields
        request.getElement("fields").appendValue(targetFieldName)
        #   d) overrides
        overrides = request.getElement("overrides")
        for ovr in overrideList:
            override = overrides.appendElement()
            override.setElement('fieldId', ovr[0])
            override.setElement('value', ovr[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            if len(overrideList)>0:
                print("Processing BDP - "+targetFieldName+' - '+str(overrideList[0]))
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE

        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    dt = msg.getElement("securityData")
                    numSecurities = dt.numValues()
                    for i in range(0, numSecurities):
                        sd = dt.getValue(i)
                        sn = sd.getElement("security").getValue()
                        fd = sd.getElement("fieldData")
                        try:
                            field = fd.getElement(0)
                            numDividendInstances = field.numValues()
                            for k in range(0,numDividendInstances):
                                dataLine=dataLineTemplate.copy()
                                dataLine['ticker']=sn
                                field_value=field.getValue(k)
                                for dividendField in dividendFields:
                                    try:
                                        dataLine[dividendField] = field_value.getElement(dividendField).getValue(0)
                                    except:
                                        dataLine[dividendField] = None
                                dataLine['Coupon Amount'] = dataLine['Coupon Amount'] * cfMultiplier
                                dataLine['Principal Amount'] = dataLine['Principal Amount'] * cfMultiplier
                                allDividends = allDividends.append(dataLine,ignore_index=True)
                        except:
                            print('Exception happened for '+sn)
                            pass

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # clean the first row and return values
        allDividends=allDividends.dropna(how='all')
        allDividends['Coupon Amount'] = allDividends['Coupon Amount'].round(decimals=10)
        allDividends['Principal Amount'] = allDividends['Principal Amount'].round(decimals=10)
        return allDividends




# SECONDARY FUNCTIONS FOR UNIVERSE GENERATION - NOT USED IN SISTEMA AS FAR AS I CAN SEE!!

def generate_universe(date_list=["20220101","20220630","20221231"], private_screen_name="FTSE100", only_index_names = False):
    '''
    :param date_list: list of dates as string in YYYYMMDD format eg ["20220101","20220630","20221231"]
    :param private_screen_name: name of private Bloomberg screen
    :param only_index_names: If True, then it takes only active index names on that period (eg keep suvivorship bias)
    :return: IndexConstituents -> a df where the columns are the constituents of the screen, the rows each of the dates, and the values whether the security is part of the screen as of that date (1) or not (None)
             weights -> df with unit weights for each date and ticker
             market cap -> df with market cap for each date and ticker
    '''

    date_format = "%Y%m%d"
    universeComposition = []
    allTickers = []

    for refDate in date_list:
        tickerList = BEQS(private_screen_name, "PRIVATE", refDate)
        allTickers = allTickers + list(set(tickerList) - set(allTickers))  # adds unique elements to allTickers
        universeComposition.append((refDate, tickerList))

    #zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    # INDEX CONSTITUENTS

    indexConstituents = _pd.DataFrame(columns=allTickers)
    for (endDateYYYYMMDD,listSecID) in universeComposition:
        row_1 = _pd.DataFrame(columns=listSecID, data=_np.ones(shape=(1, len(listSecID))))
        indexConstituents = _pd.concat([indexConstituents, row_1], axis=0, ignore_index=True)
    indexConstituents['dates']=date_list
    indexConstituents.set_index('dates',inplace=True)

    # return indexConstituents
    # zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

    #zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    # INDEX WEIGHTS

    df = _pd.DataFrame(columns=indexConstituents.columns)
    df_raw=df.copy()

    for (endDateYYYYMMDD,row) in indexConstituents.iterrows():
        endDateYYYYMMDD=str(endDateYYYYMMDD)
        # cambio 10-jun 12:56
        if only_index_names:
            listSecID=list(row[row==1].index) #esto selecciona solo los tickers que, en ese mes, forman parte del indice
        else:
            listSecID = list(row.index) #coge todos los tickers con independencia de si estan en el indice o no
        # -------------------

        listFieldID = ["CUR_MKT_CAP"]
        listFieldScale = ["RAW"]
        periodicityAdjustment = "ACTUAL"
        periodicitySelection = "DAILY"
        startDateYYYYMMDD = (_datetime.datetime.strptime(endDateYYYYMMDD, date_format) - _datetime.timedelta(days=3)).strftime(date_format)
        maxDataPoints = 1
        convertDatesToNumbers = False
        oneTablePer = "FIELD"  # "SECURITY" or "FIELD"

        response =BDH(listSecID=listSecID,
                      listFieldID=listFieldID,
                      listFieldScale=listFieldScale,
                      startDateYYYYMMDD=startDateYYYYMMDD,
                      endDateYYYYMMDD=endDateYYYYMMDD,
                      periodicityAdjustment=periodicityAdjustment,
                      periodicitySelection=periodicitySelection,
                      maxDataPoints=maxDataPoints,
                      listOverrides=[],
                      convertDatesToNumbers=convertDatesToNumbers,
                      oneTablePer=oneTablePer,
                      onlyCommonDates=False,
                      return_as_dict=False)

        totalCap = response[0].sum(1)[0]

        raw_cap=response[0].copy()
        raw_cap['date'] = response[0].index

        response[0] = response[0] / totalCap
        response[0]['date'] = response[0].index

        df = _pd.concat([df, response[0]], axis=0, ignore_index=True)
        df_raw= _pd.concat([df_raw, raw_cap], axis=0, ignore_index=True)
        print('Market cap imported for ' + response[0]['date'][0].strftime(date_format))

    weights = df.set_index('date').fillna(0)
    market_caps=df_raw.set_index('date').fillna(0)

    return [indexConstituents,weights,market_caps]


def BDS(security="CLA COMB Comdty",targetFieldName="FUT_CHAIN",overrideList=[["CHAIN_DATE","20220127"]]):
    '''
    :param security: eg "CLA COMB Comdty"
    :param targetFieldName: eg "FUT_CHAIN" , "OPT_CHAIN"
    :param overrideList: eg [["CHAIN_DATE","20220127"]] - the asof date in YYYYMMDD
    :return: returns a dataframe with the given futures or option chain for that particular date, sorted by order of contract (1st first)
    '''
    options = _misc.parseCmdLine()

    # Fill SessionOptions
    sessionOptions = _blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = _blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create the request for the historical data
        request = refDataService.createRequest("ReferenceDataRequest")

        # Fill the request
        #   a) securities
        request.getElement("securities").appendValue(security)
        #   b) fields
        request.getElement("fields").appendValue(targetFieldName)
        #   d) overrides
        overrides = request.getElement("overrides")
        for ovr in overrideList:
            override = overrides.appendElement()
            override.setElement('fieldId', ovr[0])
            override.setElement('value', ovr[1])

        # Send the request
        if False:
            print("Sending Request:", request)
        else:
            if len(overrideList)>0:
                print("Processing BDP - "+targetFieldName+' - '+str(overrideList[0]))
        session.sendRequest(request)

        # Process received events
        RESPONSE= _blpapi.Event.RESPONSE
        PARTIAL_RESPONSE= _blpapi.Event.PARTIAL_RESPONSE
        tickers=[]
        fieldValues=[]

        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(10)         #original value=500
            for msg in ev:
                #print(msg)
                if (ev.eventType()==PARTIAL_RESPONSE) or (ev.eventType()==RESPONSE):
                    dt = msg.getElement("securityData")
                    numSecurities = dt.numValues()
                    for i in range(0, numSecurities):
                        sd = dt.getValue(i)
                        sn = sd.getElement("security").getValue()
                        tickers.append(sn)
                        fd = sd.getElement("fieldData")
                        try:
                            field = fd.getElement(0)
                            # field_value=field.getValue(0)
                            for f in field:
                                fieldValues.append(f.getElementValue("Security Description"))
                        except:
                            fieldValues.append(None)

            if ev.eventType() == _blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()
        # return values
        output = _pd.DataFrame.from_records({tickers[0]:fieldValues})

        return output