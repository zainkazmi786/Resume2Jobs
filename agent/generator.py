# agent/generator.py
class ResponseGenerator:
    def __init__(self):
        self.queue = []
    
    def send_json(self, data):
        self.queue.append(f"data: {json.dumps(data)}\n\n")
    
    def generate(self):
        while self.queue:
            yield self.queue.pop(0)
        yield "data: ✅ END\n\n"