from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_bank = []
for question in question_data:
    question_bank.append(Question(question["text"], question["answer"]))

quiz = QuizBrain(question_bank)
answer = ""
while answer is not None:
    answer = quiz.next_question()
    if answer is None:
        print(f"You have answered all the questions! Your final score is {quiz.score_desc()}")
    else:
        if quiz.check_answer(answer):
            print(f"Correct! Your current score is {quiz.score_desc()}\n")
        else:
            print(f"Incorrect! Your current score is {quiz.score_desc()}\n")
