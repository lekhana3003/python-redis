# def deserialize(resp):
#     def pop(resp):
#         if len(resp) == 0:
#             raise ValueError("Missing bytes. End of input reached.")
#         return resp[0], resp[1:]
#     def skip_CRLF(resp):
#         if resp[:2] != b"\r\n":
#             raise ValueError(f"Expected CRLF. Got {resp[:2]} instead.")
#         return resp[2:]
#     def parse_operator(resp):
#         byte, resp = pop(resp)
#         return chr(byte), resp
#     def parse_int(resp):
#         byte, resp = pop(resp)
#         value = ""
#         if chr(byte) == "-" or chr(byte).isdigit():
#             value += chr(byte)
#         byte, resp = pop(resp)
#         while chr(byte).isdigit():
#             value += chr(byte)
#             byte, resp = pop(resp)
#         else:
#             resp = byte.to_bytes() + resp
#         resp = skip_CRLF(resp)
#         return value, resp
#     def parse_value(resp, byte_amount=None):
#         def add_bytes(resp, value, number_of_bytes=1):
#             for i in range(number_of_bytes):
#                 byte, resp = pop(resp)
#                 value += byte.to_bytes()
#             return value, resp
#         def parse_simple_value(resp):
#             value = b""
#             index = resp.find(b"\r\n")
#             value += resp[:index]
#             resp = resp[index:]
#             resp = skip_CRLF(resp)
#             if len(value) >= 512 * 1024 * 1024:
#                 raise ValueError("String too long. Exceeded 512MB")
#             return value, resp
#         def parse_aggregate(resp, byte_amount):
#             value = b""
#             value, resp = add_bytes(resp, value, byte_amount)
#             resp = skip_CRLF(resp)
#             return value, resp
#         if byte_amount == None:
#             value, resp = parse_simple_value(resp)
#         else:
#             value, resp = parse_aggregate(resp, byte_amount)
#         return value, resp
#     FIRST_BYTES_SIMPLE = ["+", "-", ":", "_", "#", ",", "("]
#     FIRST_BYTES_AGGREGATE = ["$", "*"]
#     operator_list = []
#     if not isinstance(resp, bytes):
#         resp = resp.encode()
#     while len(resp) > 0:
#         operator, number, value = None, None, None
#         operator, resp = parse_operator(resp)
#         if operator not in FIRST_BYTES_SIMPLE and operator not in FIRST_BYTES_AGGREGATE:
#             raise ValueError(f"Expected operator. Got {operator} instead.")
#         if operator in FIRST_BYTES_SIMPLE:
#             value, resp = parse_value(resp)
#             match operator:
#                 case ":":
#                     value = int(value.decode())
#                 case "_":
#                     if value != b"":
#                         raise ValueError(
#                             f"No extra bytes in Null allowed. Got {value} instead."
#                         )
#                     value = None
#                 case "#":
#                     if value != b"t" and value != b"f":
#                         raise ValueError(
#                             f'Only "t" and "f" for booleans allowed. Got {value} instead.'
#                         )
#                     if value == b"t":
#                         value = True
#                     if value == b"f":
#                         value = False
#         if operator in FIRST_BYTES_AGGREGATE:
#             number, resp = parse_int(resp)
#             if number != "-1":
#                 if operator == "$":
#                     value, resp = parse_value(resp, int(number))
#                 if operator == "*":
#                     value = []
#         operator_list.append([operator, number, value])
#     if len(operator_list) == 1:
#         try:
#             return operator_list[0][2].decode()
#         except:
#             return operator_list[0][2]
#     else:
#         def add_to_list(number_of_elements, operator_list, current_index):
#             result = []
#             for i in range(number_of_elements):
#                 if i + current_index >= len(operator_list):
#                     raise ValueError("Missing Array Elements")
#                 while operator_list[i + current_index][0] is None:
#                     i += 1
#                     if i + current_index >= len(operator_list):
#                         raise ValueError("Missing Array Elements")
#                 if operator_list[i + current_index][0] == "*":
#                     operator_list[i + current_index][0] = None
#                     array_length = int(operator_list[i + current_index][1])
#                     if array_length == -1:
#                         result.append(None)
#                     else:
#                         list, operator_list = add_to_list(
#                             array_length, operator_list, i + 1
#                         )
#                         result.append(list)
#                 else:
#                     if isinstance(operator_list[i + current_index][2], bytes):
#                         result.append(operator_list[i + current_index][2].decode())
#                     else:
#                         result.append(operator_list[i + current_index][2])
#                     operator_list[i + current_index][0] = None
#             return result, operator_list
#         result = []
#         for i in range(len(operator_list)):
#             if operator_list[i][0] is None:
#                 continue
#             if operator_list[i][0] == "*":
#                 operator_list[i][0] = None
#                 number_of_elements = int(operator_list[i][1])
#                 if number_of_elements == -1:
#                     result.append(None)
#                 else:
#                     list, operator_list = add_to_list(
#                         number_of_elements, operator_list, i + 1
#                     )
#                     result.append(list)
#             else:
#                 if isinstance(operator_list[i][2], bytes):
#                     result.append(operator_list[i][2].decode())
#                 else:
#                     result.append(operator_list[i][2])
#
#         return result[0]