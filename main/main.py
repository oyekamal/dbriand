from predict import Question

data = {
    "concept_uid": "113764",
    "user_id": "172337"
}

question_obj = Question()
next_question = question_obj.nextQuestion(data)
print(next_question)
