import os


class Score:
    def __init__(self, file) -> None:
        "Goes to load_maxscore() to see the last maxscore"
        self.file = file
        self.maxscore = self.load_maxscore()

    def file_is_empty(self) -> bool:
        "Returns True if there is nothing in the file -> writes 10"
        with open(self.file, "r") as file_check:
            f = file_check.read()
        if f == "":
            return True
        else:
            return False

    def save_score(self, score):
        "Saves the score if it's greater than the previous maxscore"
        print(score, self.maxscore)
        if int(score) >= int(self.maxscore):
            self.write_maxscore(str(score))

    def write_maxscore(self, score: int):
        "Write in the score.txt file if it does not exists"
        with open(self.file, "w") as file:
            file.write(str(score))
            self.maxscore = score

    def read_maxscore(self):
        "if the file exists and is not empty reads it and returns the score"
        with open(self.file, "r") as file_saved:
            last_maxscore = int(file_saved.read())
            print("Maxscore = " + str(last_maxscore))
            return last_maxscore

    def file_exists(self) -> True:
        "Check if file exists in the folder"
        if self.file in os.listdir():
            return True
        else:
            return False


    def load_maxscore(self) -> int:
        "If there is a file with a maxscore it returns it\
        so that it will be in self.maxscore,\
        otherwise it will create a new file with a maxscore of 10\
        and will return this 10"
        if self.file_exists():
            if not self.file_is_empty():
                # This reads the score and put in Puuzzle.maxscore
                maxscore = int(self.read_maxscore())
                return maxscore
            else:
                self.write_maxscore("1")
                return 3
        else:
            self.write_maxscore("1")
            return 3