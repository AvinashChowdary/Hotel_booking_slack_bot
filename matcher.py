from db import bot_db

class matcher(object):
    def __init__(self):
        self.db = bot_db()

    def score(self, list1, list2):
        score =0.0
        for hotel in list1:
            if hotel in list2:
                print(hotel)
                score = score +1.0
        if len(list1) == 0 or len(list2)==0:
            return 0
        else:
            if len(list1)>=len(list2):
                return (score/len(list1))*100
            else:
                return (score/len(list2))*100

    def match(self, obj):
        hotels = self.db.read()
        response = ""
        matches = []
        maximum=0.0
        minimum=100.0
        for hotel in hotels:
            match={}
            confidence = self.score(obj["keywords"], hotel["keywords"])
            if confidence>0:
                match["confidence"]=confidence
                match["sentence"]=hotel["sentence"]
                matches.append(match)
                if match["confidence"]<minimum:
                    minimum=match["confidence"]
                if match["confidence"]>maximum:
                    maximum=match["confidence"]
        
        threshold = maximum-((maximum-minimum)/4)
        

        matches = sorted(matches, key = lambda k: k["confidence"], reverse=True)

        for match in matches:
            print(match)
            if match["confidence"]>=threshold:
                response = response+"\n"+match["sentence"]

        return response