import json
from itertools import chain, combinations

#Use these 7 global variables to set the directories for your data and output (solution) files for each
#task.  Although I distinctly remember Dr Fagin standing on a soap box in CS210 and telling me not to use
#global variables, python doesn't have constants.  Instead, the convention is to use an all uppercase name
#to indicate to other programmers that they should only be referencing these variables, not overwring them.
#Toggle the comment between lines 7 and 8 to switch between using the example data for which I've given you
#the correct solutions and the project data for which you're asked to come up with the correct solutions.
DATA_SET=".\\data\\example\\"
#DATA_SET=".\\data\\project\\"
T1_DATA_PATH=DATA_SET+"T1\\data\\"
T1_SOLN_PATH=DATA_SET+"T1\\output\\"
T2_DATA_PATH=DATA_SET+"T2\\data\\"
T2_SOLN_PATH=DATA_SET+"T2\\output\\"
T3_DATA_PATH=DATA_SET+"T3\\data\\"
T3_SOLN_PATH=DATA_SET+"T3\\output\\"

#This function reads a priorities CSV file and returns the priorities in a single data structure
#as follows:  The top level data structure is a dictionary with two entries.  Each entry is
#indexed by a string that also serves as the prefix for each entity to be paired.  For example,
#when reading "Example Priorities File.csv", the two top level keys are 'R' (for red) and 'B' (for blue).
#The values stored in the top level dictionary are two more dictionaries.  This lower level
#dictionary is indexed by an entity name (e.g. 'B3' or 'R2' from "Example Priorities File.csv").  The
#lower level dictionary values are lists that indicate priorities from most desired to least
#desired.  For example, calling priorities['B']['B3'][1] would return 'R2' indicating that R2
#is B3's second choice mate.
def read_priorities(csv_filepath):
    priorities={}
    file=open(csv_filepath,"r")
    lines=file.read().split("\n")
    for line in lines:
        if line:
            tokens=line.split(",")
            label=tokens[0].strip(':')
            row_priorities=[]
            for token in tokens[1:]:
                if token.strip()!="":
                    row_priorities.append(token.strip())
            if label[0] in priorities:
                priorities[label[0]][label]=row_priorities
            else:
                priorities[label[0]]={}
                priorities[label[0]][label]=row_priorities
    file.close()
    return priorities

#This function prints a priorities structure from a file to the console.
def show_priorities(csv_path):
    priorities=read_priorities(csv_path)
    for key in priorities:
        for row in priorities[key]:
            print(row,end=": ")
            for col in priorities[key][row]:
                print(col,end=", ")
            print("")
        print("")
    return 0

#This funciton reads a set of pairings from a CSV file and returns a dictionary as described:
#The entities that were designated as men during pairing are used as the keys in the
#dictionary.  The values that are stored are the entities that the men ended up paired to.
#For example, after reading "Example Pairings File", pairs['B2'] would return 'R8' indicating
#B2 was paired with R8.
def read_pairs(csv_filename):
    pairs={}
    file=open(csv_filename,"r")
    lines=file.read().split("\n")
    for line in lines:
        if line:
            tokens=line.split(",")
            label=tokens[0].strip(": ")
            friends = tokens[1:]
            true_friends = []
            for friend in friends:
                if friend != []:
                    true_friends.append(friend)
            pairs[label]=true_friends
    file.close()
    return pairs

#This function writes a pairs structure (as defined in the comment for read_pairs() to a CSV
#at the filepath given as a parameter.
def write_pairs(csv_filename,pairs):
    sorted_keys=list(pairs.keys())
    sorted_keys.sort()
    of=open(csv_filename,"w")
    for man in sorted_keys:
        of.write(man)
        of.write(":,")
        of.write(pairs[man])
        of.write("\n")
    of.close()
    return 0

#This function takes the rogue couples and prints them to 
def print_rogues(output_filename, rogue_couples):
    sorted_rogues=sorted(rogue_couples)
    of=open(output_filename,"w")
    for rogue_couple in sorted_rogues:
        of.write(str(set(rogue_couple))+"\t")
    of.close()

#This function should test Hall's conditions on a graph defined in a priorities CSV file.  It
#will ensure that all members of the men set can be paired to a woman from the women set.  It
#makes no guarantees that all women can be paired to a man.  I wrote it to return "pass" or
#"fail" as strings.
def test_halls(priorities_filename,man_set_label,woman_set_label):
    #This helper function generates and returns the powerset of the input collection (with the
    #exception of null set).
    #source: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))
    
    def count_neighbors(ss, pairs):
        hood = set()
        for node in ss:
            for partner in pairs[node]:
                hood.add(partner)
        
        return len(hood)    
    
    pairs = read_pairs(priorities_filename)
    men = []
    women = []
    for node in pairs.keys():
        node : str
        if node.startswith(man_set_label):
            men.append(node)
        elif node.startswith(woman_set_label):
            women.append(node)
    if (len(men) != len(women)):
        return "fail"
    
    subsets = powerset(men)
    
    for s in subsets:
        if (len(s) > count_neighbors(s, pairs)):
            return "fail"
        
    return "pass"

#this is where you will test whether a set of proposed pairings are stable or not.  It should
#return a set of sets.  Each inner set represents a rogue pairing.  A stable pairing should
#return an empty set.
def find_rogues(pairs_filename, priorities_filename):
    pairs = read_pairs(pairs_filename)
    prio = read_priorities(priorities_filename)
    
    def get_p(node):
        return prio[node[0]][node]
    
    # print(json.dumps(prio))
    # return []
    
    tup = []
    for key in pairs.keys():
        tup.append((key, pairs[key][0]))
    pairs = tup
    
    def get_b_partner(b):
        for p in pairs:
            if p[1] == b:
                return p[0]
        print("FAAAAH! No matches!")
    
    rogues = []
    for p in pairs:
        a = p[0]
        b = p[1]
        b_prio_index = get_p(a).index(b)
        better_partners = get_p(a)[:b_prio_index]
        for new_interest in better_partners:
            new_interests_wife = get_b_partner(new_interest)
            how_much_b_likes_his_wife = get_p(new_interest).index(new_interests_wife)
            how_much_b_likes_a = get_p(new_interest).index(a)
            if (how_much_b_likes_a < how_much_b_likes_his_wife):
                rogues.append([a, new_interest])
    
    return rogues

#This is where you need to implement the Gale-Shapley algorithm on a set of priorities defined
#in a CSV file located by the csv_path parameter.  man_set_label and woman_set_label are strings
#used to label the man set and the woman set.  Each label are also used as a prefix for each
#individual man and woman.  Men propose to women and women reject men as described in the
#assigned videos.  This function should return a dictionary where the indexes are the men
#and the values are the women.

class Man:
    def __init__(self, name, pref):
        self.name = name
        self.pref = pref
        self.single = True
        self.wife = None
        self.offer_index = 0
        
    def make_offer(self):
        offer = self.pref[self.offer_index]
        self.offer_index += 1
        return offer
        
class Woman:
    def __init__(self, name, pref):
        self.name = name
        self.pref = pref
        self.husband = None
        
    def get_divorce(self):
        if (self.husband == None):
            return
        self.husband : Man
        self.husband.single = True
        self.husband.wife = None # :(
        self.husband = None
        
    def check_prefers(self, man : Man):
        if (self.husband == None):
            return True

        for option in self.pref:
            if option == self.husband.name:
                return False
            if option == man.name:
                return True
        
        print(f'Error : woman {self.name} has no preference on {man.name} or {self.husband.name}')
    

def pair(csv_path,man_set_label,woman_set_label):
    pref = read_priorities(csv_path)
    
    men = []
    women = []
    for char1 in pref.keys():
        for name in pref[char1].keys():
            person_pref = pref[char1][name]
            if name.startswith(man_set_label):
                men.append(Man(name, person_pref))
            elif name.startswith(woman_set_label):
                women.append(Woman(name, person_pref))
            else:
                print("There should only be two genders. Something is wrong.")
                print(f'\tOffending person: {name}')
    
    def get_woman(name):
        for woman in women:
            if woman.name == name:
                return woman
        print(f'Error 404 : Woman not found {name}')
    def get_man(name):
        for man in men:
            if man.name == name:
                return man
        print(f'Error 404 : Man not found {name}')


    # now, the men all put bids on the women
    done = False
    while not done: 
        done = True
        for man in men:
            man : Man
            if man.single:
                done = False
                offer = man.make_offer()
                woman : Woman = get_woman(offer)
                if woman.check_prefers(man):
                    woman.get_divorce()
                    woman.husband = man
                    man.wife = woman
                    man.single = False
    
    dictionary = {}
    for man in men:
        dictionary[man.name] = man.wife.name
        
    return dictionary
                
                    
                
        
    
#This is the main program.  For each of the three tasks you've been assigned, it has code to loop
#through all the files provided.  My suggestion is that you only use it once you have each task
#working as desired by uncommenting the calls to each task as appropriate.  Use the test() function
#as your main program as you're developing and debugging.
def main():
    def task_1():
        #test Hall's Condition for each and output results to single a file
        of=open(T1_SOLN_PATH+"results.txt","w")
        for size in (6,10,20):
            for file in range(0,4):
                of.write("size "+str(size)+" file "+str(file)+": ")
                halls_result=test_halls(T1_DATA_PATH+"size"+str(size)+"-"+str(file)+".csv",'B','R')
                of.write(str(halls_result)+"\n")
        of.close()
        print("Task 1 complete.")
        return 0            

    def task_2():
        #for each proposed pairing: find rogue pairs and print them to a file
        for size in (6,10,25,100):
            for pairing in(0,1,2,3):
                rogues=find_rogues(T2_DATA_PATH+"size_"+str(size)+"_pairings_"+str(pairing)+".csv", T2_DATA_PATH+"size_"+str(size)+"_priorities.csv")
                print_rogues(T2_SOLN_PATH+"size_"+str(size)+"_rogues_"+str(pairing)+".txt", rogues)
        print("Task 2 complete.")
        return 0
    
    def task_3():
        #generate the blue and red optimal solutions for each
        for size in (6,10,25,100):
            priorities_filename=T3_DATA_PATH+"size_"+str(size)+"_priorities.csv"
            pairs=pair(priorities_filename,'B','R')
            write_pairs(T3_SOLN_PATH+"size_"+str(size)+"_B-R_soln.csv",pairs)
            pairs=pair(priorities_filename,'R','B')
            write_pairs(T3_SOLN_PATH+"size_"+str(size)+"_R-B_soln.csv",pairs)
            print("Task 3 complete.")
        return 0
    
    # task_1()#test Hall's Condition for each
    # task_2()#find rogue pairs for each proposed
    task_3()#generate the blue and red optimal solutions for each

    return 0
   
#As stated in the comment for main(), I suggest you use this as the main program while you're
#developing and debugging.  Once you have one of your tasks working, uncomment the call to
#each task as appropriate and call main() instead of test() at the bottom by toggeling
# whether each of those lines are commented out
def test():
    return 0

#Here's where main() and/or test() gets executed when you run this script.
main()
#test()
