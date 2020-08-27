from dominos import app
from dominos.socketio_handlers import run_socketio

if __name__ == "__main__":
#     keep_client_order = parsed_args["keep_client_order"]
    keep_client_order = True
    parsed_args = None
    run_socketio(app, '0.0.0.0', keep_client_order, parsed_args)
