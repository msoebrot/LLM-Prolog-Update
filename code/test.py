from datasets import load_dataset
import pCreate as pc
import pInstance as pi
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

num_samples = 10

numbers = random.sample(range(1, length), num_samples)
#print(numbers)
sample_list = []
for num in numbers:
    sample_list += [test[num]]

#print(test[0])
#print(length)
#print(numbers)
#print(sample_list)

correct = 0
failed = 0
failed_query = 0

p_instance = []

for sample in sample_list:
    #print(sample["translation"]["en"])
    #print(sample["translation"]["ro"])
    
    print("----")
    question = str(sample["translation"]["en"]).split(";")[2].split("=")[1].strip()
    print("Question:", question)

    facts = str(sample["translation"]["en"]).split(";")[3].split("=")[1].strip().strip().split(".")
    del facts[-1]
    for i in range(len(facts)):
        #print(facts[i])
        facts[i] = str(facts[i]).split(":")[1].strip() + "."
    #print(facts)

    fact_string = "\n".join(facts)
    print("Facts:", fact_string)

    answer = (str(sample["translation"]["ro"]).split(";")[0]).split("=")[1].strip()
    print("Answer:",answer)

    username = "test"

    input_statements = "\nUsername: " + username + "\nInput:\n"+ fact_string
    prolog_list, _ = pc.create_new_facts(input_statements, "./prolog_files/kb.pl")
    prolog_string = ""
    for item in prolog_list:
        prolog_string = prolog_string + item + ".\n"
    #print(prolog_string)

    for i in range(len(prolog_list)):
        if prolog_list[-1] == ".":
            prolog_list[i] = prolog_list[i][:-1]
        #print(prolog_list[i])

    print("----")
        
    p_instance.append(pi.plInstance("master", "./prolog_files/kb.pl", save=False))

    #print(fact, "\n")
    for fact in prolog_list:
        try:
            p_instance[0].assert_fact(fact)
        except:
            failed += 1


    #print(failed)

    query_prompt = """Given the question and Prolog, make a query that would solve the question.
    Note that the list in each Prolog rule is the time it was logged, so make sure to query the variable D to capture the whole list.
    Write only the Prolog query without a period at the end or anything before it. 

    Question: """ + question + "\nExisting Rules: " + prolog_string

    #print(query_prompt)

    response = model.generate_content(query_prompt)
    query = response.text.strip()

    if "Query: " in query:
        q_split = query.split(" Query: ")
        new_fact = q_split[0].strip()
        p_instance[0].assert_fact(new_fact)
        query = q_split[0].strip()
    #print(response.text)

    print("Query:", query)
    
    try:
        q_ans = p_instance[0].query(query)
    except:
        print("Failure 1")
        try:
            time.sleep(20)
            response = model.generate_content(query_prompt)
            query = response.text.strip()
            print("New Query:", query)
            q_ans = p_instance[0].query(query)
        except:
            print("Failure 2")
            q_ans = [{"D": "Failure"}]
            failed_query += 1
    print("Query Answer: ", q_ans)

    result = ""

    if len(q_ans) > 0:
        for ans in q_ans:
            if "Failure" in ans["D"]:
                print("Prolog Fact:", prolog_string)
                result = "Failure"
            elif "Variable" in ans["D"]:
                result = "False"
            else:
                result = "True"
                break      
    else:
        result = "False"

    print("Prolog Result:", result)

    if result == answer:
        correct += 1
        print("Correct")
    else:
        print("Wrong")

    p_instance.pop()
    time.sleep(20)

print("Correct: ", correct, " / ", num_samples)