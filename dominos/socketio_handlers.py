"""Flask-SocketIO handlers and utility functions"""
import random, time, subprocess
from flask import request
from flask_socketio import send, emit#, join_room, leave_room
from dominos.Engine import Engine
from dominos import socketio

"""Settings"""
parsed_args = {}
keep_client_order = True

class RoomTracker:
    def __init__(self):
        self.game_rooms = {}
        self.sids_to_rooms = {}

rt = RoomTracker()
rt.game_rooms[1] = {"clients": {}, "observers": {}, "started": False}

"""Run Flask-SocketIO, potentially changing settings"""

def run_socketio(app, host, keep_order=None, cmd_args=None):
#     if keep_order is not None:
#         global keep_client_order
#         keep_client_order = keep_order
#     if cmd_args is not None:
#         global parsed_args
#         parsed_args = cmd_args

    socketio.run(app, host=host)

"""Utility Functions"""

# def get_id_from_sid(sid):
#     room = rt.sids_to_rooms[sid]
#     for c in rt.game_rooms[room]["clients"]:
#         if rt.game_rooms[room]["clients"][c]["sid"] == sid:
#             return c
#     raise ValueError("Invalid sid request")

# def broadcast_to_room(room):
#     def broadcast(msg, tag=None):
#         """Send a message to all clients."""
#         clear_old_info(room)
#         if tag is None:
#             socketio.send(msg, room=room)
#         else:
#             for client in rt.game_rooms[room]["clients"]:
#                 emit_to_client_in_room(room)(msg, client, tag, clear=False)
#     return broadcast

# def emit_to_client_in_room(room):
#     def emit_to_client(msg, client_id, tag=None, clear=True):
#         # Clear response before whispering, to ensure we don't keep a stale one
#         if clear:
#             rt.game_rooms[room]["clients"][client_id]["response"] = "No response"
#         if tag is None:
#             socketio.send(msg, room=rt.game_rooms[room]["clients"][client_id]["sid"])
#         else:
#             emit(tag, msg, room=rt.game_rooms[room]["clients"][client_id]["sid"])
#     return emit_to_client

# def retrieve_response_in_room(room):
#     def retrieve_response(client_id):
#         """Get the current stored response corresponding to the requested client."""
#         return rt.game_rooms[room]["clients"][client_id]["response"]
#     return retrieve_response

# def clear_old_info(room, specific_client=None):
#     # Erase outdated info
#     for client in ([specific_client] if specific_client is not None else rt.game_rooms[room]["clients"]):
#         emit_to_client_in_room(room)("", client, "error")
#         emit_to_client_in_room(room)("", client, "prompt")

"""SocketIO Handlers"""

# @socketio.on('join_room')
# def on_join(room):
#     if room not in rt.game_rooms:
#         rt.game_rooms[room] = {"clients": {}, "observers": {}, "started": False}
#     join_room(room)
#     new_index = max(rt.game_rooms[room]["clients"].keys()) + 1 if len(rt.game_rooms[room]["clients"]) > 0 else 0
#     rt.game_rooms[room]["clients"][new_index] = {"sid": request.sid, "response": "No response", "ai": False}
#     rt.sids_to_rooms[request.sid] = room
#     send("A new player has joined room {}!".format(room), room=room)

# @socketio.on('leave_room')
# def on_leave(room):
#     leave_room(room)
#     send("A player has left room {}!".format(room), room=room)

# @socketio.on('connect')
# def on_connect():
# #     new_index = max(clients.keys()) + 1 if len(clients) > 0 else 0
# #     clients[new_index] = {"sid": request.sid, "response": "No response", "ai": False}
#     print("Client connected")
# #     print(clients)

# @socketio.on('ai_connect')
# def mark_as_ai():
#     room = rt.sids_to_rooms[request.sid]
#     for c in rt.game_rooms[room]["clients"]:
#         if rt.game_rooms[room]["clients"][c]["sid"] == request.sid:
#             rt.game_rooms[room]["clients"][c]["ai"] = True
#             print("Marked {} as AI".format(c))
#             break
#     else:
#         raise Exception("Didn't mark as AI, probably executed AI connect before joining room was completed")

# @socketio.on('observer_connect')
# def mark_as_observer(room):
#     rt.sids_to_rooms[request.sid] = room
#     rt.game_rooms[room]["observers"][request.sid] = {}

# @socketio.on('start_observer')
# def start_as_observer(n_agents):
#     print(f"Waiting for {n_agents} agents to connect before starting...")
#     # Need to check here not for the number of clients, but for the number of AI, so that we give enough time
#     # to mark AIs as AI, so that we send them AI-compatible messages. Setting sleep to something low (e.g. 0.0001)
#     # and not waiting for us to mark them as AI will result in us treating them like humans,
#     # And so the agents never respond since we don't send them the correct messages.
#     # Will need to change this a bit if we want to allow human players to mix with Scheduler,
#     # Since this assumes all players from Scheduler are AIs
#     room = rt.sids_to_rooms[request.sid]
#     while len([c for c in rt.game_rooms[room]["clients"] if rt.game_rooms[room]["clients"][c]["ai"]]) < n_agents:
#         time.sleep(0.001)
#         pass
#     on_start(room)

# @socketio.on('disconnect')
# def on_disconnect():
# #     try:
# #         del game_rooms[room]["clients"][get_id_from_sid(request.sid)]
#     print("Client disconnected")
# #     except ValueError:
# #         del game_rooms[room]["observers"][request.sid]
# #         print("Observers disconnected")

@socketio.on('start_game')
def on_start():
    print("starting")
    room = 1
    winner = Engine(emit_to_client_in_room(room), broadcast_to_room(room), retrieve_response_in_room(room),
                    n_players=len(rt.game_rooms[room]["clients"])).run_game()
    socketio.stop()

@socketio.on('response')
def store_response(message):
    room = 1
    sender_id = get_id_from_sid(request.sid)
    print("Got a response from player {}: ".format(sender_id) + message)
    clear_old_info(room, sender_id)
    rt.game_rooms[room]["clients"][sender_id]["response"] = message

#################
#################
#################
#################
#################

def get_id_from_sid(sid):
    room = 1
    for c in rt.game_rooms[room]["clients"]:
        if rt.game_rooms[room]["clients"][c]["sid"] == sid:
            return c
    raise ValueError("Invalid sid request")

def broadcast_to_room(room):
    def broadcast(msg, tag=None):
        """Send a message to all clients."""
        clear_old_info(room)
        if tag is None:
            socketio.send(msg, room=room)
        else:
            for client in rt.game_rooms[room]["clients"]:
                emit_to_client_in_room(room)(msg, client, tag, clear=False)
    return broadcast

def emit_to_client_in_room(room):
    def emit_to_client(msg, client_id, tag=None, clear=True):
        # Clear response before whispering, to ensure we don't keep a stale one
        if clear:
            rt.game_rooms[room]["clients"][client_id]["response"] = "No response"
        if tag is None:
            socketio.send(msg, room=rt.game_rooms[room]["clients"][client_id]["sid"])
        else:
            emit(tag, msg, room=rt.game_rooms[room]["clients"][client_id]["sid"])
    return emit_to_client

def retrieve_response_in_room(room):
    def retrieve_response(client_id):
        """Get the current stored response corresponding to the requested client."""
        return rt.game_rooms[room]["clients"][client_id]["response"]
    return retrieve_response

def clear_old_info(room, specific_client=None):
    # Erase outdated info
    for client in ([specific_client] if specific_client is not None else rt.game_rooms[room]["clients"]):
        emit_to_client_in_room(room)("", client, "error")
        emit_to_client_in_room(room)("", client, "prompt")

#################
#################
#################
#################
#################



# def whisper(msg, player, tag=None):
#     socketio.emit(tag, msg, room=request.sid)

# def shout(msg, tag=None):
#     socketio.emit(tag, msg)

@socketio.on('connect')
def test_connect():
    print("Client connected")
    new_index = max(rt.game_rooms[1]["clients"].keys()) + 1 if len(rt.game_rooms[1]["clients"]) > 0 else 0
    rt.game_rooms[1]["clients"][new_index] = {"sid": request.sid, "response": "No response", "ai": False}
    rt.sids_to_rooms[request.sid] = 1

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
# @socketio.on('start game')
# def on_start(passed_room=None):
#     if passed_room is not None:
#         room = passed_room
#     else:
#         room = rt.sids_to_rooms[request.sid]
#     if not rt.game_rooms[room]["started"]:  # Don't allow multiple starts
#         print("Starting")
#         broadcast_to_room(room)("",  "start game")
#         rt.game_rooms[room]["started"] = True
#         # shuffle clients randomly
#         clients_keys = list(rt.game_rooms[room]["clients"].keys())
#         random_keys = [i for i in range(len(rt.game_rooms[room]["clients"]))]
#         if not keep_client_order:
#             random.shuffle(random_keys)
#         shuffled_clients = {}
#         for i, k in enumerate(random_keys):
#             shuffled_clients[k] = rt.game_rooms[room]["clients"][clients_keys[i]]
#         rt.game_rooms[room]["clients"] = shuffled_clients

#         ai_players = [c for c in rt.game_rooms[room]["clients"] if rt.game_rooms[room]["clients"][c]["ai"]]
#         print(rt.game_rooms[room]["clients"])
#         engine = Engine(emit_to_client_in_room(room), broadcast_to_room(room), retrieve_response_in_room(room),
#                         nonlocal_ais=ai_players, n_players=len(rt.game_rooms[room]["clients"]), **parsed_args)
#         winner = engine.run_game()
#         socketio.stop()

# @socketio.on('action')
# def store_action(message):
#     room = rt.sids_to_rooms[request.sid]
#     sender_id = get_id_from_sid(request.sid)
#     print("Got an action from player {}: ".format(sender_id) + message)
#     clear_old_info(room, sender_id)
#     rt.game_rooms[room]["clients"][sender_id]["response"] = message

# @socketio.on('add_bot')
# def add_bot(bot_type):
#     room = rt.sids_to_rooms[request.sid]
#     broadcast_to_room(room)(f"Adding {bot_type} to game", "info")
#     def run_agent():
#         try:
#             subprocess.run(f"python3 ./coup/agents/{bot_type}.py {room}", shell=True, check=False)
#             print('done')
#         except BaseException:
#             assert False
#             pass
# #     thread = threading.Thread(target=run_agent)
#     thread = socketio.start_background_task(target=run_agent)
# #     thread.start()
#     thread.join()

