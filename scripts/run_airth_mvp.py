from src.agents.airth_agent import AirthAgent

def main():
    print("Initializing Airth MVP...")
    airth = AirthAgent()
    print("Airth is online. Type 'quit' to exit.")
    print(f"Airth: {airth.process_input('Hello Airth, tell me about your purpose.')}") # Initial greeting

    while True:
        user_query = input("You: ")
        if user_query.lower() == 'quit':
            print("Airth is signing off.")
            break
        response = airth.process_input(user_query)
        print(f"Airth: {response}")

if __name__ == "__main__":
    main()