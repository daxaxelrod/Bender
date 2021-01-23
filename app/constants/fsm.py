states = [
    "idle",
    "selecting",
    "preparing",
    "presenting",
]

transitions = [
    {'trigger': 'wake' , 'source': 'idle', 'dest': 'selecting'},
    {'trigger': 'sleep' , 'source': 'selecting', 'dest': 'idle'},
    {'trigger': 'select_item' , 'source': 'selecting', 'dest': 'preparing', unless=["is_drink_unavailable"]},
    {'trigger': 'drink_finished' , 'source': 'preparing', 'dest': 'presenting'},
    {'trigger': 'reset' , 'source': 'presenting', 'dest': 'idle'},
]
