# streaming_executor.py
from typing import Dict, Any, Iterator, List
from langchain.schema.agent import AgentAction, AgentFinish
import traceback

class StreamingAgentExecutor:
    """A completely standalone streaming executor implementation"""
    
    def __init__(self, agent, tools, memory=None):
        self.agent = agent
        self.tools = tools
        self.memory = memory
        self.tool_map = {tool.name: tool for tool in tools}
    
    @classmethod
    def from_agent_and_tools(cls, agent, tools, memory=None):
        return cls(agent=agent, tools=tools, memory=memory)
    
    def stream(self, inputs: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Stream the execution of the agent with tools."""
        # We'll create our own intermediate steps list with proper structure
        intermediate_steps = []
        
        try:
            print("🛠️ Available tools:", [tool.name for tool in self.tools])
            
            # Main execution loop
            finished = False
            while not finished:
                # Print for debugging
                print(f"🔄 Current step: {len(intermediate_steps)}")
                if intermediate_steps:
                    print("📊 Intermediate steps structure:")
                    for i, step in enumerate(intermediate_steps):
                        print(f"  Step {i}: {type(step)}, length: {len(step) if isinstance(step, tuple) else 'N/A'}")
                
                try:
                    # Create a new, clean input for the agent
                    agent_inputs = dict(inputs)  # Make a copy
                    if self.memory:
                        memory_inputs = self.memory.load_memory_variables({})
                        agent_inputs.update(memory_inputs)
                    
                    # Direct call to the agent's LLM with our inputs
                    response = self.agent.llm_chain.run(
                        input=agent_inputs["input"],
                        intermediate_steps=intermediate_steps,
                        stop=self.agent._stop,
                    )
                    
                    print(f"🤖 Agent response: {response}")
                    
                    # Parse the response into an action or a finish
                    parsed_output = self.agent.output_parser.parse(response)
                    print(f"📝 Parsed output type: {type(parsed_output)}")
                    
                    # Check if we're done
                    if isinstance(parsed_output, AgentFinish):
                        print("✅ Agent finished")
                        yield {"type": "final_result", "output": parsed_output.return_values}
                        finished = True
                        continue
                    
                    # Ensure we have a valid action
                    if not isinstance(parsed_output, AgentAction):
                        raise ValueError(f"Expected AgentAction, got {type(parsed_output)}")
                    
                    # Clean tool name
                    tool_name = parsed_output.tool.strip()
                    print(f"🔧 Selected tool: {tool_name}")
                    
                    # Check if tool exists
                    if tool_name not in self.tool_map:
                        raise ValueError(f"Tool '{tool_name}' not found. Available: {list(self.tool_map.keys())}")
                    
                    # Signal tool start
                    yield {"type": "tool_start", "tool": tool_name, "input": parsed_output.tool_input}
                    
                    # Execute the tool
                    try:
                        tool = self.tool_map[tool_name]
                        observation = tool.run(parsed_output.tool_input)
                        
                        # Properly structure the step
                        step_tuple = (parsed_output, observation)
                        intermediate_steps.append(step_tuple)
                        
                        # Signal tool completion
                        yield {"type": "tool_end", "tool": tool_name, "output": observation}
                        
                    except Exception as e:
                        error_msg = f"Tool error in {tool_name}: {str(e)}"
                        print(f"❌ {error_msg}")
                        traceback.print_exc()
                        
                        # Signal tool error
                        yield {"type": "tool_error", "tool": tool_name, "error": error_msg}
                        
                        # Add to steps with error
                        intermediate_steps.append((parsed_output, f"Error: {str(e)}"))
                
                except Exception as e:
                    error_msg = f"Agent planning error: {str(e)}"
                    print(f"❌ {error_msg}")
                    traceback.print_exc()
                    yield {"type": "agent_error", "error": error_msg}
                    break
                    
        except Exception as e:
            error_msg = f"Stream execution error: {str(e)}"
            print(f"🔥 {error_msg}")
            traceback.print_exc()
            yield {"type": "pipeline_error", "error": error_msg}