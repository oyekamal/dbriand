import requests
import  csv
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np
import json
from gensim.parsing.preprocessing import remove_stopwords
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

import os
from django.conf import settings
import torch
from transformers import pipeline



API_KEY = "keys2wfOHFvi5WmMg"
BASE_ID = "appUQyoFtpfIjDofv"
Token = "Bearer pati8mqxK8asUrPu9.59945f88f6495279b671305a1a1d32e5202c379a32ead5646aba0341e6d83a0a"

sentiment = torch.load('ml_models/model_sentiment_analyse.pt')
sentiment_tokenizer = torch.load('ml_models/tokenizer_sentiment_analyse.pt') 
mapping_sentiment = {
    0:"A",
    1:"B",
    2:"C",
    3:"D",
    4:"E"
}



def preprocess(text, vocabulary=None):
    texts = [remove_stopwords(x)\
        .translate(str.maketrans('','',string.punctuation))\
        .translate(str.maketrans('','',string.digits))\
        for x in text]
    texts = pd.Series([stemSentence(x) for x in texts])
    texts = [' '.join([x for x in string.split()]) for string in texts]
    if vocabulary:
        vectorizer_cv = CountVectorizer(analyzer='word', vocabulary=vocabulary_)
    else:
        vectorizer_cv = CountVectorizer(analyzer='word')
    return vectorizer_cv


def stemSentence(sentence):
    porter = PorterStemmer()
    token_words = word_tokenize(sentence)
    stem_sentence = [porter.stem(word) for word in token_words]
    return ' '.join(stem_sentence)




class Question:

    def getQuestionMastery(self, uid):
        questions = []
        response = requests.get(
            url="https://api.airtable.com/v0/appUQyoFtpfIjDofv/Activities", #?fields%5B%5D=Activities&fields%5B%5D=uid 
            headers={"Authorization": Token}
        ).json()

        # for o in response["records"]:
        #     questions.append(o["fields"])
        #     if o["fields"]["Concept Id"][0] == uid:
        #         questions.append(o["fields"])
                # repp = requests.get(
                #     url="https://api.airtable.com/v0/appUQyoFtpfIjDofv/Activity%20Mastery?", #fields%5B%5D=Id&fields%5B%5D=Activty+Id&fields%5B%5D=User+Id&fields%5B%5D=Concept+Id+(from+Activty+Id)&fields%5B%5D=uid+(from+Activty+Id) 
                #     headers={"Authorization": Token}
                # ).json()
                # for oo in repp["records"]:
                #     if oo["fields"]["Activity Id"][0] == o["fields"]['uid']:
                #         questions.append(oo["fields"])
            
        return questions

    def getQuestionHistory(self, uid):
        questions = []
        response = requests.get(
            url="https://api.airtable.com/v0/appUQyoFtpfIjDofv/Activities", #?fields%5B%5D=Activities&fields%5B%5D=uid 
            headers={"Authorization": Token}
        ).json()

        for o in response["records"]:
            if o["fields"]["uid (from Concept Id)"][0] == uid:
                repp = requests.get(
                    url="https://api.airtable.com/v0/appUQyoFtpfIjDofv/Activity%20Mastery?", #fields%5B%5D=Id&fields%5B%5D=Activty+Id&fields%5B%5D=User+Id&fields%5B%5D=Concept+Id+(from+Activty+Id)&fields%5B%5D=uid+(from+Activty+Id) 
                    headers={"Authorization": Token}
                ).json()
                for oo in repp["records"]:
                    if oo["fields"]["Activity Id"][0] == o["fields"]['uid']:
                        questions.append(oo["fields"])
            
        return questions

        
    def extract_act(self, concept_uid, user_id):
        all_activities = []
        activity_mastery = []
        activity_history = []
        texts = []

        activities_obj  = []
        history_obj  = []
        mastery_obj  = {}

        with open('data/Activity.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for ptr,row in enumerate(spamreader):
                if ptr != 0:
                    if row[6] == concept_uid:
                        all_activities.append(row[0])
                        activity_mastery += row[10].split(",")
                        sentiment.eval()
                        with torch.no_grad():
                            inputs = torch.tensor(sentiment_tokenizer(row[4]).input_ids)
                            inputs = inputs.view(1,-1)
                            output = [ obj.item() for obj in sentiment(inputs)[0][0]]
                            output = mapping_sentiment.get(output.index(max(output))) 

                        activities_obj.append({
                            "Id":row[0],
                            # "Timestamp":row[2],
                            "Question":row[4],
                            "difficulty": output,
                            "count": 0,
                            "diff_time": 0,
                            "Mastery Level": 0,
                            "Assigned At": 0
                        })
                        activity_history += row[9].split(",")

        for obj in activities_obj:
            texts.append(obj["Question"])
        processor = preprocess(texts)
        processor.fit(texts)
        X = processor.transform(texts)
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(X)

        with open('data/Activity_Mastery.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for ptr,row in enumerate(spamreader):
                if row[0] in activity_mastery and user_id == row[1]:
                    # if row[3] in list(mastery_obj.keys()):
                    #     mastery_obj[row[3]]["Mastery Level"] += float(row[6])
                    #     mastery_obj[row[3]]["count"] += 1
                    # else:
                    mastery_obj[row[3]] = {"Mastery Level": float(row[6]), "Assigned At":datetime.strptime(row[5],'%Y-%m-%d %H:%M')}
        

        with open('data/Activity_Mastery_History.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for ptr,row in enumerate(spamreader):
                if row[0] in activity_history and user_id == row[1]:
                    history_obj.append({
                        "Id":row[0],
                        "Activity Id":row[3],
                        "Created At":row[5],
                        "Mastery Level":row[7],
                        "Exercise Duration":row[8],
                        "Total Duration":row[10],
                        "diff_time": float(row[10]) - float(row[8])
                    })

        for key in list(mastery_obj.keys()):
            for ptr,act in enumerate(activities_obj):
                if activities_obj[ptr]["Id"] == key:
                    activities_obj[ptr]["Mastery Level"] = mastery_obj[key]["Mastery Level"]
                    activities_obj[ptr]["Assigned At"] = mastery_obj[key]["Assigned At"]
                    activities_obj[ptr]["count"] = 0

                    # transf = processor.transform([activities_obj[ptr]["Question"]])
                    # activities_obj[ptr]["tag"] = kmeans.predict(transf)[0]

        for obj in history_obj:
            for ptr,act in enumerate(activities_obj):
                if activities_obj[ptr]["Id"] == obj["Activity Id"]:
                    activities_obj[ptr]["count"] += 1 
    
                activities_obj[ptr]["diff_time"] = obj["diff_time"] *  (activities_obj[ptr]["count"]  + 1)


        for ptr,obj in enumerate(activities_obj):
            score = ((obj["count"] +1) * 1.5)
            score += ((obj.get("diff_time", 0) +1) * 1.25)
            if obj["difficulty"] == "A":
                score += float(obj["Mastery Level"]) * 1.15
            if obj["difficulty"] == "B":
                score += float(obj["Mastery Level"]) * 1.35
            if obj["difficulty"] == "C":
                score += float(obj["Mastery Level"]) * 1.55
            if obj["difficulty"] == "D":
                score += float(obj["Mastery Level"]) * 1.75
            if obj["difficulty"] == "E":
                score += float(obj["Mastery Level"]) * 2
            activities_obj[ptr]["score"] = score

        activities_obj = list(sorted(activities_obj, key=lambda x: x["score"]))
        activities_obj = list(sorted(activities_obj, key=lambda x: x["Assigned At"]))

        return activities_obj


    def nextQuestion(self, data):
        mastery = self.extract_act(data["concept_uid"],data["user_id"])
        return mastery
    
    
if __name__ == "__main__":
    # Replace 'user_id' and 'concept_uid' with actual values
    input_data = {
        "concept_uid": "113764",
        "user_id": "172337"
    }

    question_instance = Question()
    # next_question = question_instance.nextQuestion(input_data)
   
    # print(next_question)
    print(question_instance.getQuestionMastery("recXaNeH6EcVMR6WX"))