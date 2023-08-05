from ..BBG.core import BDH
from .general import date_interval_iso as _date_interval_iso
import plotly.graph_objects as _go
import plotly.express as _px
from plotly.subplots import make_subplots as _make_subplots
import _datetime
strptime = _datetime.datetime.strptime
import pandas as pd

def plotly_subplots(rows=1, cols=1, shared_xaxes="all"):
    '''
    :param rows: number of rows in the plot
    :param cols: number of columns in the plot
    :param shared_xaxes: False, "columns", "rows" or "all"
    :return: figure with row,column suplots AND secondary axis enabled

    example: fig = plotly_subplots(2,1)
    It can then be used in combination with chart_by_axis or download_and_chart
    '''

    specs = []
    for i in range(0, rows):
        specs += [[{"secondary_y": True}] * cols]
    fig = _make_subplots(specs=specs, rows=rows, cols=cols,shared_xaxes=shared_xaxes)
    return fig


def plotly_download_and_chart(listSecID,listFieldID,yaxis=[[]],num_days=10,startDateYYYYMMDD="",endDateYYYYMMDD="",fillna=True,target_fig=None,row=1,col=1):
    '''
    :param listSecID: list of securities
    :param listFieldID: list of fields
    :param yaxis: double brackets: specify 1 or 2 depending on where we want each chart. Order =
            [
                [sec1field1, sec2field1, sec3field1]
                [sec1field2, sec2field2, sec3field2]
                etc
            ]
    :param num_days: we can specify start and end, or start + num days, or end + num days
    :param startDateYYYYMMDD:
    :param endDateYYYYMMDD:
    :param target_fig: if there is one (eg created with plotly_sublots), it can add to it; otherwise creates a 1x1
    :param row: if there is a target_fig, what row it goes into
    :param col: if there is a target_fig, what row it goes into
    :return: returns plotly fig and data as a dictionary of dfs by field
    '''
    start, end = _date_interval_iso(num_days,startDateYYYYMMDD,endDateYYYYMMDD)
    data = BDH(listSecID=listSecID,listFieldID=listFieldID,listFieldScale=[],startDateYYYYMMDD=start,endDateYYYYMMDD=end,oneTablePer="FIELD", return_as_dict=True,onlyCommonDates=False,fillna=fillna)
    print(startDateYYYYMMDD, endDateYYYYMMDD)

    if target_fig==None:
        fig=plotly_subplots(rows=1,cols=1)
    else:
        fig = target_fig

    colors = _px.colors.qualitative.Plotly[0:len(listSecID)*len(listFieldID)]
    colors = [colors[i:i + len(listSecID)] for i in range(0, len(colors), len(listSecID))]
    colors = {field:color for field,color in zip(listFieldID,colors)}
    if yaxis==[[]]:
        yaxis= {field: [len(listSecID)*False] for field in listFieldID}
    else:
        temp = {}
        for field,row in zip(listFieldID,yaxis):
            temp[field]= [True if yaxe == 2 else False for yaxe in row]
        yaxis=temp

    for field in listFieldID:
        df = data[field]
        field_axis = yaxis[field]
        field_colors = colors[field]
        for sec,axis,color in zip(listSecID,field_axis,field_colors):
            fig.add_trace(
                _go.Scatter(
                    x=df.index,
                    y=df[sec],
                    name=sec+"_"+field,
                    line_color=color),
                secondary_y= axis,
                row=row,
                col=col
            )
    return fig,data

def plotly_chart_by_axis(df_or_list_of_series=[],yaxis=[],fillna=True,target_fig=None,row=1,col=1):
    '''
    :param df_or_list_of_series: either a df or a list with each element being a pandas series
    :param yaxis: specify 1 or 2 depending on where we want each chart. Order =
                [series1, series2, series3...]
    :param target_fig: if there is one (eg created with plotly_sublots), it can add to it; otherwise creates a 1x1
    :param row: if there is a target_fig, what row it goes into
    :param col: if there is a target_fig, what row it goes into
    :return: returns plotly fig
    '''
    if isinstance(df_or_list_of_series,pd.DataFrame):
        list_of_series = [df_or_list_of_series[series] for series in df_or_list_of_series]
    else:
        list_of_series=df_or_list_of_series

    if target_fig==None:
        fig=plotly_subplots(row=row,col=col)
    else:
        fig = target_fig

    colors = _px.colors.qualitative.Plotly[0:len(list_of_series)]
    if yaxis==[]:
        yaxis= [False]*len(list_of_series)
    else:
        yaxis = [True if yaxe == 2 else False for yaxe in yaxis]

    for series,axis,color in zip(list_of_series,yaxis,colors):
        fig.add_trace(
            _go.Scatter(
                x=series.index,
                y=series,
                name=series.name,
                line_color=color),
            secondary_y= axis,
            row=row,
            col=col
        )
    return fig