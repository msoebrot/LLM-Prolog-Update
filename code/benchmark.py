from datasets import load_dataset
import time
import random
import google.generativeai as genai

dataset = load_dataset("D3xter1922/proofwriter-dataset")

train = dataset["train"]
valid = dataset["validation"]
test = dataset["test"]

length = len(test)

BARD_KEY = "AIzaSyC_cy-Qf3vSlQXVIXG0-usWuva3oW9e-yQ"

genai.configure(api_key=BARD_KEY)

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest', safety_settings=safety_settings)

numbers = random.sample(range(1, length), 10)
sample_list = []
for num in numbers:
    sample_list += [test[num]]

correct = 0

for sample in sample_list:
    
    print("----")
    question = str(sample["translation"]["en"]).split(";")[2].split("=")[1].strip()
    print("Question: ", question)

    facts = str(sample["translation"]["en"]).split(";")[3].split("=")[1].strip().strip().split(".")
    del facts[-1]
    for i in range(len(facts)):
        #print(facts[i])
        facts[i] = str(facts[i]).split(":")[1].strip() + "."
    #print(facts)

    fact_string = "\n".join(facts)
    print("Facts:", fact_string)

    answer = (str(sample["translation"]["ro"]).split(";")[0]).split("=")[1].strip()
    print("Answer: ",answer)

    username = "test"


    query_prompt = """Given the statement, output whether or not the statement in the statment is True or False according to the facts.
    Respond only with True or False. If you don't only respond with True or False, you'll be fined $50.
    Statement: """ + question + "\nExisting Rules: " + fact_string

    #print(query_prompt)

    print("----")

    response = model.generate_content(query_prompt)
    result = response.text.strip()
    print(result)

    if result == answer:
        correct += 1
        print("Correct")
    else:
        print("Wrong")

    time.sleep(15)

print("Correct: ", correct, " / 10")