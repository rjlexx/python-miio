from json import dumps as dumps_orig
from random import randint

separators = (",", ":")


def dumps(data):
    return dumps_orig(data, separators=separators)


fake_device_id = "110009025"
fake_device_model = "chuangmi.plug.v3"


def sid_to_num(sid):
    lumi, hex_id = sid.split(".")
    num_id = int.from_bytes(bytes.fromhex(hex_id), byteorder="big")
    return str(num_id)[-6:]


action_prefix = "x.scene."

# Keeping action script tail decimal int it might be used as index in some db
action_id = {
    "move": lambda sid: action_prefix + "1" + sid_to_num(sid),
    "rotate": lambda sid: action_prefix + "2" + sid_to_num(sid),
    "singlepress": lambda sid: action_prefix + "3" + sid_to_num(sid),
    "doublepress": lambda sid: action_prefix + "4" + sid_to_num(sid),
    "shake": lambda sid: action_prefix + "5" + sid_to_num(sid),
    "longpress": lambda sid: action_prefix + "6" + sid_to_num(sid),
    "flip90": lambda sid: action_prefix + "7" + sid_to_num(sid),
    "flip180": lambda sid: action_prefix + "8" + sid_to_num(sid),
    "shakeair": lambda sid: action_prefix + "9" + sid_to_num(sid),
    "taptap": lambda sid: action_prefix + "10" + sid_to_num(sid),
    "open": lambda sid: action_prefix + "11" + sid_to_num(sid),
    "close": lambda sid: action_prefix + "12" + sid_to_num(sid),
    "motion": lambda sid: action_prefix + "13" + sid_to_num(sid),
    "click": lambda sid: action_prefix + "14" + sid_to_num(sid),
    "double_click": lambda sid: action_prefix + "15" + sid_to_num(sid),
    "long_click_press": lambda sid: action_prefix + "16" + sid_to_num(sid),
}


def _inflate(
    action,
    extra,
    source_sid,
    source_model,
    target_id,
    target_ip,
    target_model,
    target_encoded_token,
    event=None,
    command_extra="",
):
    if event is None:
        event = action

    lumi, source_id = source_sid.split(".")

    return [
        [
            action_id[action](source_sid),
            [
                "1.0",
                randint(1590161094, 1590162094),
                [
                    "0",
                    {
                        "did": source_sid,
                        "extra": extra,
                        "key": "event." + source_model + "." + event,
                        "model": source_model,
                        "src": "device",
                        "timespan": ["0 0 * * 0,1,2,3,4,5,6", "0 0 * * 0,1,2,3,4,5,6"],
                        "token": "",
                    },
                ],
                [
                    {
                        "command": target_model + "." + action + "|" + source_id,
                        "did": target_id,
                        "extra": command_extra,
                        "id": randint(0, 999),
                        "ip": target_ip,
                        "model": target_model,
                        "token": target_encoded_token,
                        "value": "",
                    }
                ],
            ],
        ]
    ]

def build_open(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_magnet.v2",
):

    return dumps(
        _inflate(
            "open",
            "[1,6,1,0,[0,1],2,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )

def build_close(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_magnet.v2",
):

    return dumps(
        _inflate(
            "close",
            "[1,6,1,0,[0,0],2,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )
	
def build_click(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.v2",
):

    return dumps(
        _inflate(
            "click",
            "[1,6,1,0,[0,0],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )
	
def build_double_click(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.v2",
):

    return dumps(
        _inflate(
            "double_click",
            "[1,6,1,32768,[0,2],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )
	
def build_long_click_press(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.v2",
):

    return dumps(
        _inflate(
            "long_click_press",
            "[1,6,1,32768,[0,8],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )
	
def build_motion(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_motion.v2",
):

    return dumps(
        _inflate(
            "motion",
            "[1,1030,1,0,[0,1],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "motion",
        )
    )

def build_move(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "move",
            "[1,18,2,85,[6,256],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )


def build_flip90(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "flip90",
            "[1,18,2,85,[6,64],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )


def build_flip180(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "flip180",
            "[1,18,2,85,[6,128],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )


def build_taptap(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "taptap",
            "[1,18,2,85,[6,512],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "tap_twice",
        )
    )


def build_shakeair(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "shakeair",
            "[1,18,2,85,[0,0],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "shake_air",
        )
    )


def build_rotate(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_cube.v1",
):

    return dumps(
        _inflate(
            "rotate",
            "[1,12,3,85,[1,0],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "rotate",
            "[1,19,7,1006,[42,[6066005667474548,12,3,85,0]],0,0]",
        )
    )


def build_singlepress(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.aq3",
):

    return dumps(
        _inflate(
            "singlepress",
            "[1,13,1,85,[0,1],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "click",
        )
    )


def build_doublepress(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.aq3",
):

    return dumps(
        _inflate(
            "doublepress",
            "[1,13,1,85,[0,2],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "double_click",
        )
    )


def build_longpress(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.aq3",
):

    return dumps(
        _inflate(
            "longpress",
            "[1,13,1,85,[0,16],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
            "long_click_press",
        )
    )


def build_shake(
    source_sid,
    target_ip,
    target_encoded_token,
    target_model=fake_device_model,
    target_id=fake_device_id,
    source_model="lumi.sensor_switch.aq3",
):

    return dumps(
        _inflate(
            "shake",
            "[1,13,1,85,[0,18],0,0]",
            source_sid,
            source_model,
            target_id,
            target_ip,
            target_model,
            target_encoded_token,
        )
    )
