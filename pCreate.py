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

# Overall database
dataset = "./kb.pl"

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

At the end of each generated statement, make the last parameter is the date and time(as a 6 digit number representing hours, minutes and sceonds) 
in which the statement has been added. Therefore, the new facts you generate should have the current data applied to it as a list. Also make sure 
to not add any quotation marks in any parameter.

If the rule includes an hour range and one bound is not specified, infer from previous rules what that time should be.

If you are missing information in the new rules you have proposed, carefully look at the original input and alter
the rules generated to fit the missing information. 

I\'ll tip $20 if you perform well. Again, only respond with Prolog, in the stated statement format and space it out
with newlines. Do nothing else with the prompt."""

  model = genai.GenerativeModel('gemini-1.5-pro-latest')

  record_time = get_time()

  facts, rules, _ = get_prolog_from_file(dataset)

  fact_str = ".\n".join(fact for fact in facts)
  rule_str = ".\n".join(rule for rule in rules)


  prompt = initial_prompt + "\n\nFacts: \n" + fact_str + "\n\nRules: \n" + rule_str + \
     "\n\nCurrent Time and Date(UTC): " + record_time + input

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