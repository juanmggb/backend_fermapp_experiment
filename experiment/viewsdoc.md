## JSON Eample

{
"experiment": {
"date": "2023-07-12T10:00:00",
"author": "John Doe",
"supervisor": "Jane Smith",
"laboratory": "Example Lab",
"substrate": 1,
"microorganism": 1,
"product": 1,
"experiment_type": "kinetic",
"observations": "Some observations"
},
"variables": [
{
"variable_name": "X",
"variable_units": "unit",
"variable_type": "continuous",
"detection_method": "method",
"observations": "Variable observations",
"values": [
{
"value": 1.4,
"value_type": "measured"
},
{
"value": 1.2,
"value_type": "measured"
},
{
"value": 7.8,
"value_type": "measured"
},
{
"value": 1.9,
"value_type": "measured"
}
]
},
{
"variable_name": "Y",
"variable_units": "unit",
"variable_type": "discrete",
"detection_method": "method",
"observations": "Variable observations",
"values": [
{
"value": 1.23,
"value_type": "measured"
},
{
"value": 4.56,
"value_type": "measured"
},
{
"value": 7.89,
"value_type": "measured"
},
{
"value": 10.11,
"value_type": "measured"
}
]
}
]

}
