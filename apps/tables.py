from dash.dash_table import FormatTemplate as FormatTemplate


TOPcolumnDefs = [
    {'headerName': 'district', 'field': 'district', "filter": 'agTextColumnFilter'}, #'selectable': False, 'hideable': False, 'type': 'text',},
    {'headerName': 'Beat', 'field': 'TOP_02_beat', }, #'selectable': True, 'hideable': False, 'overflow': 'hidden'},
    {'headerName': 'Top 2% Arrest Rate', 'field': 'TOP_02_arrest_rate', "valueFormatter": {"function": "d3.format('(.2%')(params.value)"} }
 ]

BOTTOMcolumnDefs = [
    {'headerName': 'district', 'field': 'district', "filter": 'agTextColumnFilter'}, #'selectable': False, 'hideable': False, 'type': 'text',},
    {'headerName': 'Beat', 'field': 'BOTTOM_02_beat', }, #'selectable': True, 'hideable': False, 'overflow': 'hidden'},
    {'headerName': 'Bottom 2% Arrest Rate', 'field': 'BOTTOM_02_arrest_rate', "valueFormatter": {"function": "d3.format('(.2%')(params.value)"} }
 ]
defaultColDef = {
#  "filter": "agNumberColumnFilter",
"enableCellTxtSelection": True,
"ensureDomOrder": True,
 "resizable": True,
 "sortable": True,
 "editable": False,
 "floatingFilter": True,
}

opt_channel_col = [
    {'name': '', 'id': 'index', 'selectable': False, 'hideable': False, 'type': 'text',},
    {'name': 'Television', 'id': 'tv_S', 'selectable': False, 'hideable': False, 'type': 'numeric', 'format': {'specifier': ','}},
    {'name': 'Out of Home', 'id': 'ooh_S', 'selectable': False, 'hideable': False, 'type': 'numeric', 'format': {'specifier': ','}},
    {'name': 'Print', 'id': 'print_S', 'selectable': False, 'hideable': False, 'type': 'numeric', 'format': {'specifier': ','}},
    {'name': 'Facebook', 'id': 'facebook_S', 'selectable': False, 'hideable': False, 'type': 'numeric', 'format': {'specifier': ','}},
    {'name': 'Search', 'id': 'search_S', 'selectable': False, 'hideable': False, 'type': 'numeric', 'format': {'specifier': ','}}
 ]

opt_channel_col_cond = [
    {'if':{'column_id':'index'}, 'maxWidth':'60px', 'textAlign':'left', 'backgroundColor': 'white', 'fontWeight': 'bold'},
    {'if':{'column_id':'tv_S'},'maxWidth':'50px', 'textAlign':'right'},
    {'if':{'column_id':'ooh_S'},'maxWidth':'50px', 'textAlign':'right'},
    {'if':{'column_id':'print_S'},'maxWidth':'50px', 'textAlign':'right'},
    {'if':{'column_id':'facebook_S'},'maxWidth':'50px', 'textAlign':'right'},
    {'if':{'column_id':'search_S'},'maxWidth':'50px', 'textAlign':'right'},
    ]

tooltip_data_list=[
{
            'index': 'Edit these fields to set the minimum value you would spend for the month per channel.',
        },
        {
            'index': 'Edit these fields to set an approximate WEEKLY value for each channel for the first week of the month.',
        },
        {
            'index': 'Edit these fields to set an approximate WEEKLY value for each channel for the second week of the month.',
        },
        {
            'index': 'Edit these fields to set an approximate WEEKLY value for each channel for the third week of the month.',
        },
        {
            'index': 'Edit these fields to set an approximate WEEKLY value for each channel for the forth week of the month.',
        },
        {
            'index': 'Edit these fields to set the maximumm value you would spend for the month per channel.',
        }
    ]


df_col_data_cond = [
    {
            'if': {'row_index': 0},
            'backgroundColor': 'rgb(220, 220, 220)',
        },
    {
            'if': {'row_index': 5},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
]
