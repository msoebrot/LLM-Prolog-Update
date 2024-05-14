import pInstance as pi
import pCreate as pc

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

# Create a prolog instance that adds in inforamtion from the base knowledge base
p = pi.plInstance(username)

# Given a text input including the statements and the username, populates the prolog database 
p.add_rules_from_input(input_statements)

# Translate sample statements into prolog statements
test, _ = pc.create_new_facts(input_statements)
for item in test:
    print(item)

#Testing appending single statement
print("---------")

new_input = """
Username: michael

Input:

The pool will be open from 9am to 5pm on Wednesday.
"""
# openingHours(pool, wednesday, 0900, 1700, [2024, 5, 13])
new_fact, _ = pc.create_new_facts(new_input)
print(new_fact)
for fact in new_fact:
    p.assert_fact(fact)

# Prints all the facts in rules within the knowledgebase
# print(p) 

### Viability that recent works

print("---------")

print("?-openingHours(pool, monday, Y, Z, D).")
print(p.query("openingHours(pool, monday, Y, Z, D)", recent=True))

print("---------")

p.assert_fact("openingHours(pool, monday, 0900, 1700, [2024, 5, 14])")

print("?-openingHours(pool, monday, Y, Z, D).")
print(p.query("openingHours(pool, monday, Y, Z, D)", recent=True))

### Show difference what happens when recent is True or false

print("---------")

print("?-openingHours(pool, X, Y, Z, D).")
print(p.query("openingHours(pool, X, Y, Z, D)", recent=True)) # Setting recent to false makes it a string.

print("---------")

print("?-openingHours(pool, X, Y, Z, D).")
for result in p.query("openingHours(pool, X, Y, Z, D)", recent=False): # Now we get all possible opening hours.
    print(result)

print("---------")

print("?-cuisineAt(monday, lunch, C, L, D).")
for result in p.query("cuisineAt(monday, lunch, C, L, D)", recent=False): # Same here.
    print(result)

print("---------")