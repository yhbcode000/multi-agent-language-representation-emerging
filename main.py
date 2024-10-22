import requests
import random

class LLMClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def ask_chatbot(self, content, agent, data):
        url = f"{self.base_url}/ask"
        payload = {
            "content": content,
            "agent": agent,
            "data": data
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_session_list(self):
        url = f"{self.base_url}/history"
        response = requests.get(url)
        return response.json()

    def delete_session(self, session_id):
        url = f"{self.base_url}/history"
        payload = {"session_id": session_id}
        response = requests.delete(url, json=payload)
        return response.json()

    def create_new_session(self):
        url = f"{self.base_url}/history"
        response = requests.put(url)
        return response.json()

    def change_session(self, value):
        url = f"{self.base_url}/config/runtime.current_session_id"
        payload = {"value": value}
        response = requests.post(url, json=payload)
        return response.json()

    def get_agent_list(self):
        url = f"{self.base_url}/agent"
        response = requests.get(url)
        return response.json()
    

def simulate_small_town_conversation(client, agents, max_calls):
    # Initialize the system with background information
    system_data = {"background": "discuss about emerging knowledge of AI"}

    # Track how many ask function calls have been made
    ask_call_count = 0

    while ask_call_count < max_calls:
        # Choose a random agent to initiate the conversation
        initiating_agent = random.choice(agents)
        
        # Pick another agent to talk to (excluding the initiating agent)
        possible_receivers = [agent for agent in agents if agent != initiating_agent]
        if not possible_receivers:
            break  # If there's no other agent to talk to, stop the loop
        receiving_agent = random.choice(possible_receivers)

        # Initiating agent sends a message to the receiving agent
        content = f"You are Agent {initiating_agent[0]} speaking to Agent {receiving_agent[0]}."
        data = system_data.copy()
        data[f"{initiating_agent[0]}_said_something"] = content

        # Make the "ask" function call for the initiating agent
        print(f"\nCalling 'ask' for Agent {initiating_agent[1]} (Session ID: {initiating_agent[0]})")
        client.change_session(initiating_agent[0])
        response = client.ask_chatbot(content=content, agent=initiating_agent[1], data=data)
        print(f"Response from {initiating_agent[1]}: {response['message']}\n")
        
        # Let the receiving agent respond to the message
        print(f"\nCalling 'ask' for Agent {receiving_agent[1]} (Session ID: {receiving_agent[0]})")
        client.change_session(receiving_agent[0])
        receiving_response = client.ask_chatbot(content=response['message'], agent=receiving_agent[1], data=system_data)
        print(f"Response from {receiving_agent[1]}: {receiving_response['message']}\n")
        print("-"*80)
        print("-"*80)

        # Append the conversation to the system data for further interactions
        system_data.update({f"{receiving_agent[0]}_said_something": receiving_response['message']})

        # Track the number of ask function calls made
        ask_call_count += 2  # Two interactions per cycle (initiator and receiver)


def main():
    client = LLMClient()  # Initialize the client

    # Define the number of sessions to create
    n = 5  # This can be adjusted based on your needs
    
    # Create sessions and associate them with the agent "base"
    agent_names = ["base"] * n  # All agents have the name "base"
    session_ids = [client.create_new_session().get('session_id') for _ in range(n)]

    # Create agents tuples (session_id, agent_name)
    agents = list(zip(session_ids, agent_names))
    
    # Output the created agents
    print("Created agents:")
    for session_id, agent_name in agents:
        print(f"Session ID: {session_id}, Agent Name: {agent_name}")
    
    # Ask user input for the desired number of ask function calls
    while True:
        try:
            max_calls = int(input("\nEnter the desired number of ask function calls or 0 to exit: "))
            if max_calls == 0:
                print("Exiting program.")
                break
            # Simulate the small-town conversation with agents
            simulate_small_town_conversation(client, agents, max_calls)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    

# Example invocation of the main function
if __name__ == "__main__":
    main()
