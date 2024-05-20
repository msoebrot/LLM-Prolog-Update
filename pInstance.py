from pyswip import Prolog
import pCreate as pl

def most_recent(qList):
    recent = [0, 0, 0]
    result = {}

    key_name = ""

    temp = qList[0]
    for key in temp.keys():
        if type(temp[key]) == list:
            key_name = key
            break

    if key_name == "":
        return "Fail! Make sure that the date list is set to one variable (D = [2024, 05, 20])", recent

    for q in qList:
        date = q[key]
        for i in range(len(date)):
            if recent[i] < date[i]:
                recent = date
                result = q
    return result, recent

class plInstance:
    def __init__(self, name, dataset, save=False) -> None:
        self.dataset = dataset
        self.user = name
        self.save = save
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

    def set_user(self, name):
        self.user = name

    def add_rules_from_input(self, input):

        # Given an input statement with the username and three new statements, creates a list of rules using Gemini
        new_facts, self.log_time = pl.create_new_facts(input, self.dataset)

        #self.userfile = open(self.filename, "a") 
        if self.save:
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
        if self.save:
            self.userfile = open(self.filename, "a") 
            self.userfile.write(input + ".\n")
            self.userfile.close()

        self.facts.append(input)
        self.pl.assertz(input)

        return True
    
    def retract(self, statement):
        self.pl.retract(statement)
    

    def query(self, statement, recent=False):

        results = list(self.pl.query(statement))
        if recent:
            result, _ = most_recent(results)
            answer = result
        else:
            answer = results

        return answer

    