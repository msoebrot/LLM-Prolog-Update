from pyswip import Prolog
import pCreate as pl

def most_recent(qList):
  recent = [0, 0, 0]
  result = {}
  for q in qList:
    date = q["D"]
    for i in range(len(date)):
      if recent[i] < date[i]:
        recent = date
        result = q
  return result, recent

class plInstance:
    def __init__(self, name) -> None:
        self.dataset = "./kb.pl"
        self.user = name
        self.pl = Prolog()
        self.log_time = ""
        self.filename = self.user + ".pl"
        self.userfile = None
        self.facts = []
        self.rules = []

        # Gets facts, rule and the most recent log time of a prolog file
        self.facts, self.rules, self.log_time = pl.get_prolog_from_file(self.dataset)

        for fact in self.facts:
            #print(fact)
            self.pl.assertz(fact)

        for rule in self.rules:
            #print(rule)
            self.pl.assertz(rule)
    
    def __str__(self):
        fact_str = ".\n".join(fact for fact in self.facts)
        rule_str = ".\n".join(rules for rules in self.rules)
        result_str = "Facts:\n\n" + fact_str + "\n\nRules:\n\n" + rule_str
        return result_str

    def add_rules_from_input(self, input):

        # Given an input statement with the username and three new statements, creates a list of rules using Gemini
        new_facts, self.log_time = pl.create_new_facts(input)

        #self.userfile = open(self.filename, "a") 
        self.userfile = open(self.filename, "w") 
        for fact in new_facts:
            self.userfile.write(fact + ".\n")
        self.userfile.close()

        for fact in new_facts:
            self.facts.append(fact)
            self.pl.assertz(fact)

        self.log_time = pl.get_time()
        
        return True
    
    def assert_fact(self, input):
       #Given valid
       self.userfile = open(self.filename, "a") 
       self.userfile.write(input + ".\n")
       self.userfile.close()

       self.facts.append(input)
       self.pl.assertz(input)

       return True

    def query(self, statement, recent=False):

        results = list(self.pl.query(statement))
        if recent:
            result, _ = most_recent(results)
            answer = result
        else:
            answer = results

        return answer

    