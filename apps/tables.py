from dash.dash_table import FormatTemplate as FormatTemplate


defaultColDef = {
#  "filter": "agNumberColumnFilter",
"enableCellTxtSelection": True,
"ensureDomOrder": True,
 "resizable": True,
 "sortable": True,
 "editable": False,
 "floatingFilter": True,
}

TOPcolumnDefs = [
    {'headerName': 'district', 'field': 'district', "filter": 'agTextColumnFilter'},
    {'headerName': 'Beat', 'field': 'TOP_02_beat'},
    {'headerName': 'Top 2% Arrest Rate', 'field': 'TOP_02_arrest_rate', "valueFormatter": {"function": "d3.format('(.2%')(params.value)"}}
 ]

BOTTOMcolumnDefs = [
    {'headerName': 'district', 'field': 'district', "filter": 'agTextColumnFilter'},
    {'headerName': 'Beat', 'field': 'BOTTOM_02_beat'},
    {'headerName': 'Bottom 2% Arrest Rate', 'field': 'BOTTOM_02_arrest_rate', "valueFormatter": {"function": "d3.format('(.2%')(params.value)"}}
 ]

crime_type_columnDefs = [
    {'headerName': 'Rank', 'field': 'rank_of_crime_type'},
    {'headerName': 'Primary Crime Type', 'field': 'primary_type'},
    {'headerName': 'Count of Crimes in 2020', 'field': 'cnt_of_primary_typ_2020' }
 ]

crime_type_by_community_columnDefs = [
    {'headerName': 'Primary Crime Type', 'field': 'primary_type'},
    {'headerName': 'Community Area', 'field': 'community_area'},
    {'headerName': 'Count in 2020', 'field': 'cnt_of_primary_typ_2020' },
    {'headerName': 'Count in Jan 2021', 'field': 'cnt_jan_2021' }
 ]
top_streets_columnDefs = [
    {'headerName': 'Ward No', 'field': 'ward'},
    {'headerName': 'Street Name', 'field': 'street', "filter": 'agTextColumnFilter'},
    {'headerName': 'Domestic Crimes', 'field': 'domestic_crimes' }
 ]

time_columnDefs = [
    {'headerName': 'Time Perion', 'field': 'time_period'},
    {'headerName': 'Most Commong Crime', 'field': 'most_common_crime_type'},
    {'headerName': 'Arrest Rate', 'field': 'overall_arrest_rate', 'valueFormatter': {"function": "d3.format('(.2%')(params.value)"}}
 ]