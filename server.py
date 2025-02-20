
from llama_cpp import Llama
import os
from flask import Flask, request, jsonify, redirect
from config import model_path, model, chat_format

app = Flask(__name__)

llm = Llama(
      model_path=f"{model_path}{model}",
      chat_format=f'{chat_format}',
      n_gpu_layers=-1,
      # seed=1337, # Uncomment to set a specific seed
      #n_batch=4096,
      n_ctx=4096, 
      #max_tokens=4096, # use None for unlimited tokens
      stop_word=False
)


@app.route('/v1/models', methods=['POST', 'GET'])
@app.route('/models', methods=['POST', 'GET'])
@app.route('/available_models', methods=['POST'])
def models_available():
    # return a list of models available
    return os.listdir(model_path)

@app.route('/autogen', methods=['POST'])
def autogen():
    # I don't know why it must to be here, but hey who cares
    print('autogen server connected')
    return 'autogen server connected'


@app.route('/v1/completions', methods=['POST'])
#@app.route('/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
@app.route('/autogen/chat/completions', methods=['POST', 'GET'])
@app.route('/chat/completions', methods=['POST', 'GET'])
def autogen_chat_completion():
    print('content received')
    response = request.get_json()
    content =  response.get('messages', [])
    
    if len(content) == 2:
        content
    
    elif len(content) >= 4:
        content = [content[0], content[1], content[-2], content[-1]]
        
    else: 
        content = [content[0], content[1], content[-1]]
    
    chat_response = llm.create_chat_completion(
        messages=content,
        stop=None,
        temperature=0.6,
    ) 
    
    print("\n\ncontent: \n", content)
    print()
    print()
    print()
    print()
    print(chat_response)
    return chat_response





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, )

