import json, time
from mido import Message, open_output
from filter_aircraft import haversine_distance
from midi_utils import midi_scale, map_to_midi_scale


C_MIN_SCALE = midi_scale('C', 'MINOR', 'C1', 'Eb5')
DATA = "json/aircraft.json"
DRIVER = "IAC Driver Bus 1"
IN_AIR = {}

# distance between 0-7, map to velocity
# altitude between 350 - 35000, map to pitch/note

def map_value(value, min_value, max_value, min_result, max_result):
    # Check if value is outside the original range
    if value < min_value or value > max_value:
        raise ValueError(f"Input value {value} is outside the original range")

    # Calculate the percentage of value within the original range
    percentage = (value - min_value) / (max_value - min_value)

    # Map the percentage to the new range and round the result to the nearest integer
    result = round(min_result + percentage * (max_result - min_result))
    return result


def create_midi_on_msg(plane_distance, altitude, fence_distance, callsign):
    velocity = map_value(plane_distance, 0, fence_distance, 0, 127)
    # note = map_value(altitude, 100, 40000, 24, 100)
    note = map_to_midi_scale(altitude, C_MIN_SCALE, 900, 39000)
    print(f"~~~note is ***velocity: {velocity}, note: {note}***")
    on = Message("note_on", note=note, velocity=velocity, time=1)
    IN_AIR[callsign] = note
    return on

def send_midi(outport, msg):
    outport.send(msg)

def send_midi_and_reset(msg, port_name):
    outport = open_output(port_name)
    outport.send(msg)
    time.sleep(2)
    outport.reset()

def read_json_and_send_to_ableton(fence, outport):
    current = []
    with open(DATA, "r") as f:
        aircraft = json.load(f).get("aircraft")
        for i in aircraft:
            if "lat" not in i or "lon" not in i:
                continue
            lat = i.get("lat")
            lon = i.get("lon")
            i["distance"] = haversine_distance(lat, lon)
            callsign = i.get("flight", "").strip()
            if i["distance"] < fence and callsign:
                current.append(callsign)
                if not IN_AIR.get(callsign):
                    print("---plane info:")
                    print(callsign, i["distance"], i["altitude"])
                    on = create_midi_on_msg(i["distance"], i["altitude"], fence, callsign) 
                    print(f">>>sending on for {callsign}")
                    send_midi(outport, on)
    turn_off = set(IN_AIR.keys()) - set(current)
    for callsign in turn_off:
        print(f">>>turning off {callsign}...")
        note = IN_AIR.get(callsign)
        msg = Message("note_off", note=note, time=0, velocity=0)
        outport.send(msg)
        del IN_AIR[callsign]
    print("currently in air:")
    print(IN_AIR)


if __name__ == "__main__":
    outport = open_output(DRIVER)
    try:
        while True:
            read_json_and_send_to_ableton(10, outport)
            time.sleep(2)
            print("-----------------------------------")
    except KeyboardInterrupt:
        print("goodbye!")
        outport.reset()
