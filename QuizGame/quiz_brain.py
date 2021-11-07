class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def next_question(self):
        if self.question_number >= len(self.question_list):
            return None
        else:
            current_question = self.question_list[self.question_number].text
            self.question_number += 1
            answer = input(
                f"Q.{self.question_number} {current_question} (True/False):")
            return answer

    def check_answer(self, answer):
        correct = answer == self.question_list[self.question_number - 1].answer
        if correct:
            self.score += 1
        return correct

    def score_desc(self):
        return f"{self.score}/{len(self.question_list)}"
