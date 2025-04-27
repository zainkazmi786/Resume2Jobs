# llmbp.py
from flask import Blueprint, request, Response, make_response, stream_with_context, jsonify
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import the base_agent instead of the wrapped agent
from agent.agentinitializer import agent, base_agent, tools, memory
# from agent.callbacks import ToolStreamingCallbackHandler
# from agent.generator import ResponseGenerator
import json 
from threading import Thread
import traceback
llm_bp = Blueprint('llm', __name__)

latest_prompt_data = {}  # Global or better: use session, cache, or state storage

@llm_bp.route("/prepare-stream", methods=["POST", "OPTIONS"])
def prepare_stream():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200
    data = request.get_json()
    filename = data.get("filename")
    prompt   = data.get("prompt")

    if not filename or not prompt:
        return jsonify({"error": "filename and prompt are required"}), 400

    latest_prompt_data["filename"] = filename
    latest_prompt_data["prompt"] = prompt
    return jsonify({"message": "Ready to stream"}), 200

@llm_bp.route("/stream-process", methods=["GET"])
def stream_process():
    print("Available tools:", [t.name for t in tools])
    for tool in tools:
        print(f"Tool {tool.name}: {tool.__class__.__name__}")
    filename = latest_prompt_data.get("filename")
    prompt = latest_prompt_data.get("prompt")
    
    if not filename or not prompt:
        return jsonify({"error": "No prompt data found"}), 400

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    resume_path = os.path.join(project_root, "Resumes", filename)
    user_input = f"Please extract the profile from this resume at ({resume_path}) and {prompt}"
    memory.chat_memory.clear()

    def generate():
        try:
            # Use base_agent.invoke directly instead of streaming
            response = base_agent.invoke({"input": user_input})
            # response = agent.invoke({"input": user_input})
            # Send the thinking process as stream events
            thinking_steps = response.get("intermediate_steps", [])
            
            for i, (action, observation) in enumerate(thinking_steps):
                # Tool start
                yield f"data: 🛠 Starting {action.tool}...\n\n"
                # Format tool input if it's complex
                tool_input = action.tool_input
                if isinstance(tool_input, dict):
                    tool_input = json.dumps(tool_input, indent=2)
                yield f"data: 📝 Input: {tool_input}\n\n"
                
                # Tool result
                yield f"data: ✅ {action.tool} completed\n\n"
                # Format observation if it's complex
                if isinstance(observation, dict):
                    observation = json.dumps(observation, indent=2)
                yield f"data: 📋 {observation}\n\n"
            
            # Final answer
            yield f"data: 🎉 Final result: {response['output']}\n\n"
            
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            yield f"data: 🔥 Pipeline error: {str(e)}\n\n"
            yield f"data: 📜 Traceback: {trace}\n\n"
        finally:
            yield "data: ✅ END\n\n"

    response = Response(stream_with_context(generate()), content_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    return response


# llmbp.py
# @llm_bp.route("/stream-tools", methods=["POST"])
# def stream_tools():
#     data = request.get_json()
#     # ... (input validation and path resolution logic)
    
#     generator = ResponseGenerator()
#     callback = ToolStreamingCallbackHandler(generator)
    
#     def agent_thread():
#         try:
#             base_agent.run(
#                 input=user_input,
#                 callbacks=[callback],
#                 include_run_info=True
#             )
#         except Exception as e:
#             generator.send_json({
#                 "type": "error",
#                 "message": str(e),
#                 "traceback": traceback.format_exc()
#             })
#         finally:
#             generator.send_json({"type": "end"})
    
#     Thread(target=agent_thread).start()
    
#     return Response(
#         stream_with_context(generator.generate()),
#         mimetype="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive"
#         }
#     )