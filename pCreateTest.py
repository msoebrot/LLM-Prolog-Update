from pyswip import Prolog
import pCreate as pl
import pInstance as pi

dataset = "./kb.pl"
username = "michael"

# Sample input
input_statements = """
Username: michael

Input:

The pool will be open for 2 more hours longer on Monday from now on.
The pool opens at 2 pm the day on Tuesday and closes at 7.
It takes me 25 minutes to walk from the parking lot to the engineeering building.
The engineering building has 7 floors.
There will be road construction on I-280 for the first week of July."""

# Gets facts, rule and the most recent log time of a prolog file
facts, rules, log_time = pl.get_prolog_from_file(dataset)

# Given an input statement with the username and three new statements, creates a list of rules using Gemini
new_facts, _ = pl.create_new_facts(input_statements, dataset)

filename = username + ".pl"
userfile = open(filename, "a") 
for fact in new_facts:
  userfile.write(fact + ".\n")
userfile.close()

prolog = Prolog()

print("---------")
print("Facts:")

for fact in facts:
  print(fact)
  prolog.assertz(fact)

print("---------")
print("Rules:")

for rule in rules:
  print(rule)
  prolog.assertz(rule)


print("---------")
print("New Facts:")
for fact in new_facts:
  print(fact)
  prolog.assertz(fact)

print("---------")
print("Testing:\n")
print("?-openingHours(pool, monday, Y, Z, D)")

for q in prolog.query("openingHours(pool, monday, Y, Z, D)"):
  print(q)

print("---")

qDict = list(prolog.query("openingHours(pool, monday, Y, Z, D)"))
for q in qDict:
  print(q)

print("---")

result, recent = pi.most_recent(qDict)
print(str(result) + ": " + str(recent))

print("---------")