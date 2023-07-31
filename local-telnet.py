import requests
import socket
import atexit
import os
global server

user = "User:"
bot = "Bot:"
ENDPOINT = "http://127.0.0.1:5001"
conversation_history = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
def get_prompt(user_msg):
    return {
        "prompt": f"{user_msg}",
        "use_story": False, 
        "use_memory": False, 
        "use_authors_note": False, 
        "use_world_info": False, 
        "max_context_length": 2048,
        "max_length": 80,
        "rep_pen": 1.0,
        "rep_pen_range": 2048,
        "rep_pen_slope": 0.7,
        "temperature": 0.7,
        "tfs": 0.97,
        "top_a": 0.8,
        "top_k": 0,
        "top_p": 0.5,
        "typical": 0.19,
        "sampler_order": [6,0,1,3,4,2,5], 
        "singleline": False,
        "sampler_seed": 69420, # Use specific seed for text generation?
        "sampler_full_determinism": False, # Always give same output with same settings?
        "frmttriminc": False, #Trim incomplete sentences
        "frmtrmblln": False, #Remove blank lines
        "stop_sequence": ["\n\n\n\n\n", f"{user}"]
        }
def handle_client(client_socket):
    try:
        client_socket.send(user.encode('utf-8'))
        while True:
            user_message = client_socket.recv(1024).decode('utf-8').strip()

            if len(user_message) < 1:
                bot_response = f"{bot}Please provide a valid input.\n"
            else:
                fullmsg = f"{conversation_history[-1] if conversation_history else ''}{user} {user_message}\n{bot} "
                prompt = get_prompt(fullmsg)
                response = requests.post(f"{ENDPOINT}/api/v1/generate", json=prompt)
                if response.status_code == 200:
                    results = response.json()['results']
                    text = results[0]['text']
                    response_text = text.split('\n')[0].replace("  ", " ")
                    conversation_history.append(f"{fullmsg}{response_text}\n")
                    bot_response = f"{bot} {response_text}\n"
                else:
                    bot_response = f"{bot} Unable to generate a response.\n"
            client_socket.send(bot_response.encode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
def main():
    os.system(f"clear")
    server.listen(5)
    print("Telnet server started. Listening for connections...")
    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"Connection established with {client_address}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.close()
def close_socket():
    server.close()
if __name__ == "__main__":
    atexit.register(close_socket)
    main()
