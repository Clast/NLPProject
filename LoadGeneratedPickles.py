#Run me after you run Phase1 to generate the knowledgebases

import pickle
import string
import operator
import os

with open('knowledge_base.pickle', 'rb') as handle:
    knowledge_base = pickle.load(handle)

with open('words_to_articles.pickle', 'rb') as handle:
    words_to_articles = pickle.load(handle)

#Example
possible_target_article = {}
query = "is there construction at utd"

dir = "/Users/MeghanaVellaturi/Desktop/NLPProject/NLPProject/words_to_article.pickle"
dir = os.getcwd()
dir1 = os.path.join(dir,'/Desktop/NLPProject/NLPProject/')
with open(dir + '/' + "keys.txt", 'w') as f:

    for word in words_to_articles:
        f.write("{")
        f.write('"value": "{}"'.format(word))
        #print("\n")
        f.write("},\n")

for word in query.split():
    if word in words_to_articles:


        contained = words_to_articles[word]

        print(word + " is located in: ")
        for k in contained:
            print(k)

        for k in contained:
            highestscore = 0
            score = knowledge_base[k][2][word]
            print ("Importance score is: " + str(score) + " in article" + k)
            if k not in possible_target_article:
                possible_target_article[k] = score
            else:
                possible_target_article[k] += score
                print("")


target_article = max(possible_target_article.items(), key=operator.itemgetter(1))[0]
print(target_article + " has the highest importance score with " + str(possible_target_article[target_article]))
print("")

print("Title: " + knowledge_base[target_article][0])
print("URL: " + knowledge_base[target_article][1])
summary = knowledge_base[target_article][3]
print("Summary: ")
for listitem in summary:
    print(listitem)


