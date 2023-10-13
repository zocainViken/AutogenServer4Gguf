
from llama_cpp import Llama
import os
from flask import Flask, request, jsonify, redirect
from config import model_path

app = Flask(__name__)

#model_path = 'F:/path/to/ur/folder/'# folder must contain only .gguf
model_path = model_path

@app.route('/available_models', methods=['POST'])
def models_available():
    # return a list of models available
    return os.listdir(model_path)

@app.route('/autogen', methods=['POST'])
def autogen():
    # I don't know why it must to be here, but hey who cares
    print('autogen server connected')
    return redirect("/autogen/chat/completions")



@app.route('/autogen/chat/completions', methods=['POST', 'GET'])
def autogen_chat_completion():
    # so basicaly the main function to create completions
    data=request.json
    #print("input data: \n", data)
    #print()

    if data['model']:
        model_name = data['model']
    else:
        model_name = "model.gguf"
    print('model name: ' + model_name)
    print()

    temperature = data['temperature']
    max_tokens = 4096
    stop = []

    dialogue = """"""
    messages = data['messages']
    
    for i in messages:
        #print(i['role'].replace('\n\n', ''))
        dialogue = dialogue + i['role'].replace('\n', '') + ':\n'
        #print(i['content'].replace('\n\n', ''))
        dialogue = dialogue + i['content'].replace('\n\n', '')
        dialogue = dialogue + '\n\n\n'
    
    print('dialogue:\n', dialogue)
    print()

    llm = Llama(model_path=model_path+model_name)
    output = llm(
        f"{dialogue}",
        max_tokens=int(max_tokens),
        stop=stop,
        echo=True,
        temperature=temperature
    )
    
    print('output:')
    print()
    print(jsonify(output))
    print('\n\n\n\n')
    
    return jsonify(output)
    





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, )





