from pyswip import Prolog
import pCreate as pc
import time

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
condensed_facts = []
group_size = 50
for i in range(0, len(facts), group_size):
    count = count + 1
    fact_group = ""
    for j in range(group_size):
        if i + j < len(facts):
            fact_group = fact_group + facts[i + j] + "\n"
        else:
            break
    condensed_facts += [fact_group]

prolog_list = []

print("----------------------------------------------------")
print("Generating Prolog... \n")
counter = 0
start = time.time()
for statement in condensed_facts:
    
    counter = counter + 1

    input_statements = "\nUsername: " + username + "\nInput:\n"+ statement
    test, _ = pc.create_new_facts(input_statements, "./prolog_files/kb.pl")
    tst_string = ""
    for item in test:
        tst_string = tst_string + item + ".\n"
    prolog_list += test

    num = counter * group_size
    end = time.time()
    length = end - start
    print("Statements done:", num)
    print("Time elapsed:", length, "seconds", "\n")
    start = time.time()
    time.sleep(15) #Delay to avoid going over request limit for Google Gemini API
    

output_file = "test_files/valid_prolog_test_output.txt"
userfile = open(output_file, "w") 
for fact in prolog_list:
    userfile.write(fact + ".\n")
userfile.close()

#print("----------------------------------------------------")

#print("Generated Prolog Facts: \n")
failed = 0
for fact in prolog_list:
    #print(fact, "\n")

    try:
        prolog = Prolog()
        prolog.assertz(fact)
    except:
        failed += 1

print("----------------------------------------------------")

print("Total Facts:", len(prolog_list))
print("Failed:", failed)

exit(0)



