# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from circle.paths.v1_banks_wires_id_instructions import Api

from circle.paths import PathValues

path = PathValues.V1_BANKS_WIRES_ID_INSTRUCTIONS