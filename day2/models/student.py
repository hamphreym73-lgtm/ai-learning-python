class Student:

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def show_info(self):
        print("name:", self.name)
        print("score:", self.score)

    def update_score(self, score):
        if 0 <= score <= 100:
            self.score = score
            return True
        else:
           return False

    def is_passed(self):
        return self.score >= 60

    def __str__(self):
        return f"name:{self.name},{self.score}分"

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["score"])