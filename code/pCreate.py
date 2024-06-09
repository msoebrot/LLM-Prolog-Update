# Helper functions for converting natural language to Prolog. Also includes function for
# converting Prolog files into statements

import pathlib
import textwrap
import time
import os

import google.generativeai as genai
# from pyswip import Prolog

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

# Overall database
dataset = "./prolog_files/kb.pl"

# print("---------")

# print("Models:")

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

#### HELPER FUNCTIONS ####

# Returns the current time
def get_time():
  return time.ctime()

# Gets prolog from a file and returns the list of rules and facts, along with the most recent update time.
def get_prolog_from_file(filename):
  f = open(filename, "r")
  dataset_str = f.read()
  
  split = dataset_str.split("% Facts")
  data_split = split[1].split("% Rules")
  for i in range(len(data_split)):
    data_split[i] = data_split[i].strip()

  time = split[0].strip()

  facts_str = data_split[0]
  facts = facts_str.replace(".", "").split("\n")
  
  rules_str = data_split[1]
  rule_list = rules_str.replace(".", "").split("\n")
  while '' in rule_list:
    rule_list.remove('')
  for rule in rule_list:
    if '%' in rule:
      rule_list.remove(rule)
  rules = rule_list

  return facts, rules, time

def text_to_prolog(input, dataset):
  initial_prompt = """Convert all statements from plaintext into Prolog statements. Only respond with Prolog.
Assume other relevant rules exist. You should format the prolog statements based on the existing facts and ruls that exist in the knowledge base.
If the question includes \"I\" or \"me\", set the name of the user as the subject. The X is just a letter X.

Make sure to create for every single input statements as missing one would call for a $100 fine. If similiar structures
already exist within the facts, try to generate similar structures while also keeping in mind the rules that are able
to use theses facts. If other parts of the fact are not mentioned, do not change from the existing facts. Altering when
not mentioned in the input is bad and should also incur a $50 fine.

After you have generated some rules, look over them again and make sure that the information matches what is intended from the input string.
Losing meaning or accidently giving false information within the facts will result in a $50 fine.

Make sure that important informations such as subject names are retained within the generated facts. 
If there is a measurement, that the metric is mentioned within the head of the rule to retain that measurement.
Do not mix in numbers with words inside of the body, as it will cause errors.
For example:

"The height of the statue of liberty is 305 feet." => height_in_feet(statue_of_liberty, 305, [date_list])
"In Fall 2023, UCSC had a 30 percent of undergraduates were Asian" => percent_of_undergraduates(ucsc, asian, 30, [date_list])
"Nvidia stock has jumped 240 percent over the past year" => year_percent_increase(Nvidia, stock, 240, [date_list])
"Amazon has over 1.6 million employees" => number_of_employees(Amazon, 1600000, [date_list])

If the statement consists of a series of descriptors, you can put them in a list.

For example:
"At Niagara Falls, the scenery is beautiful, but also loud" => scenery(niagara_falls, [beautiful, loud]], [date_list])
"Disneyland is known for its' fun atmosphere and thrilling rides" => known_for(disneyland, [fun, thrilling_rides]], [date_list])

At the end of each generated statement, make the last parameter is the date and time(as a 6 digit number representing hours, minutes and sceonds) 
in which the statement has been added. Therefore, the new facts you generate should have the current data applied to it as a list. Also make sure 
to not add any quotation marks in any parameter.

In rules in which a comparison is being made, make sure the comparison is stated within the rule head.
This goes for adverbs as well, as losing this could change the sentence.
Ex. Michael is as rich as Joe => as_rich_as(michael, joe, [date_list])
Ex. John's hand were about the size of textbooks => about_the_size(john, hand, textbook, [date_list])
Ex. Most of Bob's time is spent fishing => most_of_free_time(bob, fishing, [date_list])

An example for the date_list looks like: [date_list] = [current_year, current_month, current_date, 6-digit-time]
Ex. If it is currently March 4th, 2024 at 16:00:00, date_list is [2024, 03, 04, 160000]


If the rule includes an hour range and one bound is not specified, infer from previous rules what that time should be.

If you are missing information in the new rules you have proposed, carefully look at the original input and alter
the rules generated to fit the missing information. 

I\'ll tip $20 if you perform well. Again, only respond with Prolog, in the stated statement format and space it out
with newlines. Do nothing else with the prompt."""

  model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest', safety_settings=safety_settings)

  record_time = get_time()

  facts, rules, _ = get_prolog_from_file(dataset)

  fact_str = ".\n".join(fact for fact in facts)
  rule_str = ".\n".join(rule for rule in rules)


  prompt = initial_prompt + "\n\nFacts: \n" + fact_str + "\n\nRules: \n" + rule_str + \
     "\n\nCurrent Time and Date(UTC): " + record_time + input

  response = model.generate_content(prompt)

  while len(response.candidates[0].content.parts) < 1:
    print("pCreate failed response:", input)
    time.sleep(15)
    response = model.generate_content(prompt)

  return prompt, response.text, record_time

def create_new_facts(input, dataset):
  prompt, response, recorded_time = text_to_prolog(input, dataset)

  new_facts = response.replace(".", "").split("\n")
  while '' in new_facts:
    new_facts.remove('')

  for i in range(len(new_facts)):
    new_facts[i] = new_facts[i].strip()
  
  return new_facts, recorded_time