
from llama_cpp import Llama
import os
from flask import Flask, request, jsonify, redirect
from config import model_path, MODEL

app = Flask(__name__)


def talk(llm, dialog, stop, max_tokens=4096, temperature=0):
    output = llm(
        f"{dialog}",
        max_tokens=int(max_tokens),
        stop=stop,
        echo=True,
        temperature=temperature
    )
    # remove input from output
    output['choices'][0]['text'] = output['choices'][0]['text'][len(dialog):]
    output['choices'][0]['message'] = output['choices'][0]['text']
    
    return output

def tweaked_talk(llm, dialog, stop, data, idx, max_tokens=4096, temperature=0):
    def slicer(data, idx):
        similarity = ''
        prepromt = ''
        dialogue = ''
        for index, item in enumerate(data['messages']):
            if str(item) != similarity:
                similarity = str(item)
                if index == 0:
                    prepromt = f"role: {item['role']}\n{item['content']}\n\n"
                elif index <= idx and index >= 2:
                    dialogue = dialogue + ''
                else:
                    dialogue = dialogue + f"role: {item['role']}\n{item['content']}\n\n"
            else:
                pass

        dialogue = prepromt + dialogue
        return dialogue  # Return the updated 'dialogue' variable

    v = idx
    # Check token size
    for i in range(0, 90):
        if len(llm.tokenize(slicer(data, v).encode())) >= 4096 and v < len(data['messages']):
            v *= 2  # Update the value of 'v' in the loop
            text = slicer(data, v).encode()
            vtc = len(llm.tokenize(text))
            
        else:
            break

    dialogue = slicer(data, v)
    print('\ntweaked dialogue: \n', dialogue)
    print('#############################################################################\n#############################################################################\n\n\n')
    output = talk(llm, dialogue, stop, max_tokens, temperature)
    return output



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

# openai api 
# /v1/embeddings
# /images/create_variation
# /images/generate
# /v1/audio/speech
# /v1/audio/transcriptions # -> speech to text whisper.cpp ?
# /v1/audio/translations
# /v1/chat/completions

@app.route('/v1/completions', methods=['POST'])
@app.route('/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
@app.route('/autogen/chat/completions', methods=['POST', 'GET'])
def autogen_chat_completion():
    # so basicaly the main function to create completions
    data=request.json

    if data['model']:
        model_name = data['model']
    else:
        model_name = MODEL
    print('model name: ' + model_name)
    print()

    # Check if the 'model' key exists in the data dictionary
    if 'temperature' in data:
        # The 'model' key is present, so you can safely access its value
        temperature = data['temperature']
    else:
        # Handle the case when 'model' key is not present
        temperature = 0

    max_tokens = 4096
    stop = []

    dialogue = """"""
    messages = data['messages']
    
    for i in messages:
        dialogue = dialogue + i['role'].replace('\n', '') + ':\n'
        dialogue = dialogue + i['content'].replace('\n\n', '')
        dialogue = dialogue + '\n\n\n'
    
    llm = Llama(model_path=model_path+model_name)
    context = int(len(llm.tokenize(dialogue.encode())))

    idx = 3
    if context <= max_tokens - 1:
        
        print('\nstandard dialogue: \n', dialogue)
        print('#############################################################################\n#############################################################################\n\n\n')
        output = talk(llm, dialogue, stop, max_tokens, temperature)
        return jsonify(output)
    
    else:
        print('too much tokens, sorry but the start of you\'re chat will be ignored')
    
        output = tweaked_talk(llm, dialogue, stop, data, idx, max_tokens, temperature)
        return jsonify(output)






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, )

