import json
import time
user = "User:"
bot = "Bot:"
ENDPOINT = "https://horde.koboldai.net"
conversation_history = []
apikey = "0000000000"
print("===\nStarting...\n")
def get_prompt(user_msg):
    return {
        "models": [],
        "params": {
            "n": 1,
            "max_context_length": 700,
            "max_length": 80,
            "rep_pen": 1.1,
            "temperature": 0.55,
            "top_p": 0.9,
            "top_k": 0,
            "top_a": 0,
            "typical": 1,
            "tfs": 1,
            "rep_pen_range": 512,
            "rep_pen_slope": 0.7,
            "sampler_order": [6, 0, 1, 2, 3, 4, 5],
        },
        "prompt": f"{user_msg}",
    }
def getResponse():
    while True:
        try:
            response = make_url_request((f"{ENDPOINT}/api/v2/generate/text/status/{current_id}"), method='GET')
            if response and response.get('done', False):
                response = make_url_request((f"{ENDPOINT}/api/v2/generate/text/status/{current_id}"), method='GET')
                return response
            else:
                time.sleep(1)
        except Exception as e:
            print(f"An error occurred during polling: {e}")
            return None

def make_url_request(url, data=None, method='POST'):
    import urllib.request
    try:
        request = None
        headers = {"apikey": apikey,'User-Agent':'Horde Terminal Interface v1','Client-Agent':'HordeTermInt:1'}
        if method=='POST':
            json_payload = json.dumps(data).encode('utf-8')
            request = urllib.request.Request(url, data=json_payload, headers=headers, method=method)
            request.add_header('Content-Type', 'application/json')
        else:
            request = urllib.request.Request(url, headers=headers, method=method)
        response_data = ""
        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode('utf-8')
            json_response = json.loads(response_data)
            return json_response
    except urllib.error.HTTPError as e:
        try:
            errmsg = e.read().decode('utf-8')
            print(f"Error: {e} - {errmsg}, Make sure your Horde API key and worker name is valid.")
        except Exception as e:
            print(f"Error: {e}, Make sure your Horde API key and worker name is valid.")
        return None
    except Exception as e:
        print(f"Error: {e} - {response_data}, Make sure your Horde API key and worker name is valid.")
        return None

while True:
    try:
        user_message = input(f"{user}")
        if len(user_message.strip()) < 1:
            print(f"{bot}Please provide a valid input.")
            continue
        fullmsg = (f"{conversation_history[-1] if conversation_history else ''}{user} {user_message}\n{bot} ")
        prompt = get_prompt(fullmsg)
        current_id = None
        current_payload = None
        current_generation = None
        pop = make_url_request((f"{ENDPOINT}/api/v2/generate/text/async"), prompt)
        print(f"{pop}\n")
        if not pop:
            print(f"Failed to fetch job from {ENDPOINT}. Waiting 5 seconds...")
            time.sleep(5)
            continue
        current_id = pop['id']
        response = getResponse()
        response_text = None
        if response:
            gen = response['generations']
            text = gen[0]['text']
            response_text = text.split('\n')[0].replace("  ", " ")
            conversation_history.append(f"{fullmsg}{response_text}\n")
            print(f"{bot} {response_text}")
        if response_text == ' no valid completions':
            print(f"{response}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"\n-------\n{response}")

