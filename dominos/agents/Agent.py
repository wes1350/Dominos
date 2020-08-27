"""Base class for Agents."""
import json

if __name__ == "Agent":
    from utils.game import *
#     from utils.network import *
else:
    from .utils.game import *
#     from .utils.network import *

class Agent:
    def __init__(self, **kwargs):
        # Set base Agent properties
        properties = {"verbose": False, "tag": ""}
        for prop in properties:
            self.__setattr__(prop, properties[prop])
        # Override default properties with passed in values
        for arg in kwargs:
            if arg in properties:
                self.__setattr__(arg, kwargs[arg])
            else:
                raise ValueError(f"Unexpected argument: {arg}")

    def __str__(self):
        return type(self).__name__ + (("_" + self.tag) if self.tag else "")

    def update_wrapper(self, event):
        event_info = json.loads(event) if isinstance(event, str) else event
        if isinstance(event_info, str):
            event_info = json.loads(event_info)
            if "info" in event_info:
                if isinstance(event_info["info"], str):
                    event_info["info"] = json.loads(event_info["info"])
        else:
            if "info" in event_info:
                if isinstance(event_info["info"], str):
                    event_info["info"] = json.loads(event_info["info"])
        if self.verbose:
            print("Updating with event: ", json.dumps(event_info, indent=4))
        self.update(event_info)

    def update(self, event):
        pass

    def react(self, event_type : str, options : dict):
        options = json.loads(options) if isinstance(options, str) else options
        if event_type == "action":
            response = self.decide_action(options)
        else:
            if not isinstance(event_type, str):
                raise ValueError("event_type must be a string type")
            else:
                raise ValueError("Received unknown event type: " + event_type)
        if response is None:
            raise Exception(("Agent did not return a value for its response. "
                             "Make sure to return a value when choosing a response."))
        if self.verbose:
            print("Reacting to:", json.dumps(options, indent=4))
            print("Sending response", response, type(response))
        return response

    def unimplemented_response(self, event_type : str):
        def raiser(options):
            raise NotImplementedError("Responding to " + event_type + " not implemented")
        return raiser

    def decide_action(self, options):
        return self.unimplemented_response("actions")(options)
