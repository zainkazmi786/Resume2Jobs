# agent/callbacks.py
from langchain.callbacks.base import BaseCallbackHandler
import json

class ToolStreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, generator):
        self.generator = generator
        
    def on_tool_start(self, serialized, input_str, **kwargs):
        self.generator.send_json({
            "type": "tool_start",
            "tool": serialized["name"],
            "input": input_str
        })

    def on_tool_end(self, output, **kwargs):
        self.generator.send_json({
            "type": "tool_end",
            "output": output
        })