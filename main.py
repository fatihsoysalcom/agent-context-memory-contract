import time

class StatelessAgent:
    """
    Simulates an AI agent that processes each prompt independently,
    without retaining any memory of past interactions.
    This agent lacks a 'memory contract'.
    """
    def __init__(self, name="StatelessBot"):
        self.name = name

    def process_prompt(self, user_input: str) -> str:
        print(f"[{self.name} - Processing (no memory)] User: {user_input}")
        time.sleep(0.1) # Simulate processing time

        # Simulate LLM-like response based *only* on current input
        if "my name is" in user_input.lower():
            name = user_input.split("my name is")[-1].strip().split(" ")[0].replace(".", "")
            return f"Hello, {name}! How can I help you today?"
        elif "what is my name" in user_input.lower():
            # This demonstrates the agent losing context: it forgets the name from the previous turn.
            return "I don't know your name. Please tell me again."
        elif "favorite color" in user_input.lower():
            return "I don't have a favorite color, as I am an AI."
        else:
            return "I'm not sure how to respond to that."

class MemoryAgent:
    """
    Simulates an AI agent that maintains a simple 'memory contract'
    by storing and retrieving key information from past interactions.
    """
    def __init__(self, name="MemoryBot"):
        self.name = name
        self.memory = {} # Simple dictionary to store key facts
        self.conversation_history = [] # To store full conversation for context

    def _update_memory(self, user_input: str, agent_response: str):
        # This method represents part of the 'memory contract' - systematically storing information.
        if "my name is" in user_input.lower():
            name = user_input.split("my name is")[-1].strip().split(" ")[0].replace(".", "")
            self.memory["user_name"] = name
            print(f"[{self.name} - Memory Update] Stored user_name: {name}")
        
        # Store full conversation history for potential RAG-like context in future prompts
        self.conversation_history.append(f"User: {user_input}")
        self.conversation_history.append(f"Agent: {agent_response}")

    def process_prompt(self, user_input: str) -> str:
        print(f"[{self.name} - Processing (with memory)] User: {user_input}")
        time.sleep(0.1) # Simulate processing time

        # Construct a "context" for the current turn, simulating RAG or prompt engineering
        # This is how the 'memory contract' is leveraged to provide relevant past information.
        context = ""
        if self.memory:
            context += "Known facts:\n"
            for key, value in self.memory.items():
                context += f"- {key}: {value}\n"
        
        # Add recent conversation history as context
        if self.conversation_history:
            context += "\nRecent conversation:\n"
            context += "\n".join(self.conversation_history[-4:]) # Last 4 turns as context

        # Simulate LLM-like response using current input and context
        response = ""
        if "what is my name" in user_input.lower():
            # The agent uses its 'memory' to answer the follow-up question correctly.
            if "user_name" in self.memory:
                response = f"Based on our previous conversation, your name is {self.memory['user_name']}."
            else:
                response = "I don't recall your name. Could you please tell me?"
        elif "my name is" in user_input.lower():
            name = user_input.split("my name is")[-1].strip().split(" ")[0].replace(".", "")
            response = f"Hello, {name}! It's good to know your name."
        elif "favorite color" in user_input.lower():
            response = "I don't have a favorite color, as I am an AI. What's yours?"
        else:
            response = "I'm not sure how to respond to that, even with my memory."

        self._update_memory(user_input, response) # Update memory after generating response
        return response

def run_simulation():
    print("--- Simulating Stateless Agent (No Memory Contract) ---")
    stateless_agent = StatelessAgent()
    
    # Interaction 1: User introduces themselves
    response1_stateless = stateless_agent.process_prompt("Hi, my name is Elara.")
    print(f"Agent Response: {response1_stateless}\n")

    # Interaction 2: User asks a follow-up question that requires memory
    response2_stateless = stateless_agent.process_prompt("What is my name?")
    print(f"Agent Response: {response2_stateless}\n")
    # Expected: Agent will forget Elara's name because it has no memory contract.

    print("\n--- Simulating Memory Agent (With Memory Contract) ---")
    memory_agent = MemoryAgent()

    # Interaction 1: User introduces themselves
    response1_memory = memory_agent.process_prompt("Hello, my name is Kaan.")
    print(f"Agent Response: {response1_memory}\n")

    # Interaction 2: User asks a follow-up question that requires memory
    response2_memory = memory_agent.process_prompt("What is my name?")
    print(f"Agent Response: {response2_memory}\n")
    # Expected: Agent will remember Kaan's name due to the memory contract.

    # Interaction 3: Another question to show continued memory
    response3_memory = memory_agent.process_prompt("Do you have a favorite color?")
    print(f"Agent Response: {response3_memory}\n")

if __name__ == "__main__":
    run_simulation()
