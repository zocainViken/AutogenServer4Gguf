# Autogen Chat Completions For Llama_cpp.gguf

This project provides an API for generating chat completions using the Llama model. It utilizes Flask to create a server that can be accessed to generate responses based on input data.

## Setup

To set up the project, follow the steps below:

1. Clone the repository to your local machine.

```bash
git clone https://github.com/zocainViken/AutogenServer4Gguf.git
```

2. Ensure you have Python installed.
3. Install the necessary requirements using the following command:

```bash
python -m pip install -r requirements.txt
```


## Usage

To use the API for generating chat completions, follow the steps below:

1. Ensure that the necessary model path files with the .gguf extension are placed in the specified folder.
then this folder path must be specified into config.py and that should do it.
2. Run the Flask server by executing the following command:

```bash
python server.py
```


3. Access the server at the specified address and port to generate chat completions.

## Endpoints

1. `/available_models` - This endpoint return a list of available models.
2. `/autogen` - This endpoint is for connection verification.
3. `/autogen/chat/completions` - This endpoint is used to create completions based on the input data.


## finale code to launch the server
```bash
pyton -m pip install -r requirements.txt
```
```bash
python server.py
```
## example of client side code
```json
OAI_CONFIG_LIST example
[
    {
        "model":"model0.gguf",
        "api_base": "http://127.0.0.1:5000/autogen",
        "api_type": "open_ai",
        "api_key": "NULL"
    },
    {
        "model":"model1.gguf",
        "api_base": "http://127.0.0.1:5000/autogen",
        "api_type": "open_ai",
        "api_key": "NULL"
    },
    {
        "model":"model2.gguf",
        "api_base": "http://127.0.0.1:5000/autogen",
        "api_type": "open_ai",
        "api_key": "NULL"
    }
]
```


## Python part 
```python
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {
    "request_timeout":600,# set up here if response took too long and you got some errorn but 600 seems to be fair
    #"retry_wait_time" :500,
    #"max_retry_period" :400,
    "seed":13,# number for cache folder name
    "config_list":config_list,
    "temperature":0.3# creativity: 0 -> 1 & 1 = very creative 
}


assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
                            "user_proxy",
                            code_execution_config={
                                                "work_dir": "coding",
                                                "use_docker":"false"# to avoid some error because the code won't launc| true is default value
                                                }
                           )


user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# This initiates an automated chat between the two agents to solve the task
```

## License

Yeah I don't really know what does that mean soooo...
do what you can




## https://github.com/ggerganov/llama.cpp
## https://github.com/abetlen/llama-cpp-python
## https://github.com/microsoft/autogen
