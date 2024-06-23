import json
import boto3

def a12():
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client



    bedrock_model_id = "ai21.j2-ultra-v1" #the model ID of the model to use

    prompt = "What is the largest city in England?" #the prompt to send to the model

    body = json.dumps({
        "prompt": prompt, #AI21
        "maxTokens": 1024, 
        "temperature": 0, 
        "topP": 0.5, 
        "stopSequences": [], 
        "countPenalty": {"scale": 0 }, 
        "presencePenalty": {"scale": 0 }, 
        "frequencyPenalty": {"scale": 0 }
    }) #build the request payload


    response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Bedrock

    response_body = json.loads(response.get('body').read()) # read the response

    response_text = response_body.get("completions")[0].get("data").get("text") #extract the text from the JSON response

    print(response_text)


def calsue():
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime',region_name="us-east-1") #creates a Bedrock client


    image_message = {
        "role": "user",
        "content": [
            { "text": "Please describe the image of an apple." }
        ],
    }


    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages = [image_message],
        inferenceConfig = {
            "maxTokens": 1024,
            "temperature": 0,
        },
    )

    response_message = response.get("messages")[0].get("content")
    print(json.dumps(response_message, indent=2))







calsue()

