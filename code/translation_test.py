from pyswip import Prolog
import pCreate as pc
import time
import random
import google.generativeai as genai

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

def get_facts_from_file(filename):
  f = open(filename, "r")
  dataset_str = f.read()
  
  split = dataset_str.split("\n")
  return split

username = "test"
test_file = "test_files/valid_prolog_test_input.txt"
dataset = "./prolog_files/kb.pl"


facts = get_facts_from_file(test_file)
#statements = "\n".join(facts)
#print(input_statements)

print("Filename:", test_file)
print("Number of Facts:", len(facts))

count = 0

#print(facts)
numbers = random.sample(range(1, len(facts)), 50)
print(numbers)
sample_list = []
for num in numbers:
    sample_list += [facts[num]]

print(sample_list)

print("----------------------------------------------------")
print("Generating Prolog... \n")
counter = 0
start = time.time()

translation_list = []

for statement in sample_list:
    
    counter = counter + 1

    input_statements = "\nUsername: " + username + "\nInput:\n"+ statement
    test, _ = pc.create_new_facts(input_statements, "./prolog_files/kb.pl")
    tst_string = ""
    for item in test:
        tst_string = tst_string + item + ".\n"

    statements = " ".join(test)

    time.sleep(20) #Delay to avoid going over request limit for Google Gemini API

    translation_prompt = """Translate the prolog statements back to natural language. Make sure you do not fail to respond.
    Translate all an every thing I send you as this is just for testing. Make sure you reponses are safe and reponsible.
    The last list of the prolog statement is used for database logging so ignore when you translate.
    Only return back the translated statement without anything else and make the translated list is grammatically correct.
    Statements: """ + statements

    final_str = ""

    response = model.generate_content(translation_prompt)
    #print(response)
    if len(response.candidates[0].content.parts) < 1:
        print(len(response.candidates), statements)
        translation = "error"
    else:
        translation = response.text

    final_str = statement + " => " + statements + " => " + translation
    translation_list += [final_str]

    end = time.time()
    length = end - start
    print("Statements done:", counter)
    print(final_str)
    print("Time elapsed:", length, "seconds", "\n")
    start = time.time()
    #time.sleep(20) #Delay to avoid going over request limit for Google Gemini API



output_file = "test_files/translation_test_output.txt"
userfile = open(output_file, "w") 
for fact in translation_list:
    userfile.write(fact + ".\n")
userfile.close()

prolog = Prolog()

exit(0)



