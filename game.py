import csv, random, string
from rich.console import Console
from rich.table import Table
from rich import box

class Game:
    """
    Command Line Quiz Game
    """
    TRUE_STATEMENTS = ["y", "yes", "t", "true"]

    console = Console(log_path=False, log_time=False, highlight=False)

    def __init__(self, filename:str="db.csv", questionCount:int=10) -> None:
        """
        Args:
            filename: str = Name of the csv file containing the questions
            questionCount: int = Maximum no. of questions to display
        """
        self.gameOver: bool = False
        self.questions: list
        self.questionCount: int = questionCount
        self.questionIndex: int = 0
        self.filename: str = filename
        self.gameScore: int = 0
        self.highScore: int = 0
        self.wrongCount: int = 0
        self.skipCount: int = 0
        self.get_questions()

    def get_questions(self) -> None:
        """
        Load questions
        """
        with open(self.filename, "r") as csv_file:
            self.questions = list(csv.reader(csv_file))[1:]
        
        while [] in self.questions:
            self.questions.remove([])

        random.shuffle(self.questions)
        if len(self.questions) >= self.questionCount:
            self.questions = random.sample(self.questions, self.questionCount)
        else:
            self.questionCount = len(self.questions)
        for i, q in enumerate(self.questions):
            self.questions[i] = list(map(str.strip, q))


    def resetGame(self) -> None:
        """
        Reset the game and its parameters, while keeping track of highscore
        """
        self.highScore = max(self.highScore, self.gameScore)
        self.gameOver = False
        self.questions = []
        self.gameScore = 0
        self.wrongCount = 0
        self.questionIndex = 0
        self.skipCount = 0
        self.get_questions()

    def display_score(self) -> None:
        scoreBoard = [
            f"[green]Score: {self.gameScore}[/green]",
            f"[cyan]Left: {self.questionCount - self.questionIndex}[/cyan]",
            f"[indian_red]Skipped: {self.skipCount}[/indian_red]"
                if self.skipCount > 0
                else None,
            f"[red]Failed: {self.wrongCount}[/red]",
            f"[yellow]Highscore: {self.highScore}[/yellow]"
                if self.highScore > 0
                else None,
        ]
        scoreBoard = filter(bool, scoreBoard)
        scoreTable = Table(show_header=False, box=box.SIMPLE_HEAD)
        scoreTable.add_row(*scoreBoard)
        self.console.log(scoreTable)
        # self.console.log("--" * 40)
        # self.console.log("\t\t".join(scoreBoard))
        # self.console.log("--" * 40)

    def display_question(self) -> bool:
        """
        Returns True if question was answered with a valid option
        """
        if self.questionIndex >= self.questionCount:
            raise IndexError("questionIndex out of range!")
        row = self.questions[self.questionIndex]
        question, answer, reason = row[0], row[1], row[-1]
        answer = answer.strip()
        options = [option.strip() for option in row[1:-1]]
        random.shuffle(options)
        answer_option = string.ascii_uppercase[options.index(answer)]

        options = dict(zip(string.ascii_uppercase, options))
        self.console.log(
            f"[yellow]Q{self.questionIndex+1}.[/yellow] [green]{question}[/green]"
        )
        for ordinal, option in options.items():
            self.console.log(f"[cyan]{ordinal})[/cyan] {option}")

        selected_option = self.console.input(
            "[bright_magenta]Select an option >>> [/bright_magenta]"
        ).upper()

        if selected_option == "":
            self.skipCount += 1
            self.console.log(
                f"[yellow]Correct answer is option [{answer_option}] '{answer}'[/yellow]"
            )
        elif selected_option not in options:
            self.console.log("[red]Invalid Option![/red]")
            self.questionIndex -= 1
        else:
            if options[selected_option] == answer and selected_option == answer_option:
                self.console.log("[green]Correct Answer![/green]")
                self.gameScore += 1
            else:
                self.console.log(
                    f"[red]Wrong Answer![/red] [yellow]Answer is option [{answer_option}] '{answer}'[/yellow]"
                )
                self.wrongCount += 1
            if reason not in ["None", None, "NULL", "", " "]:
                self.console.log(f"[yellow]Reason:[/yellow] {reason}")

        self.console.log("--" * 40, end="\n\n")
        self.questionIndex += 1

    def start(self) -> None:
        while not self.gameOver:
            while self.questionIndex < self.questionCount:
                self.console.clear()
                self.display_score()
                self.display_question()
                self.console.input("Press [cyan]ENTER[/cyan] to continue.")
            else:
                self.console.clear()
                t = Table(show_header=False, box=box.HORIZONTALS)
                t.add_column()
                t.add_column()
                t.add_row("[cyan]Your Score:[/cyan] ", f"[green]{self.gameScore}[/green]")
                t.add_row("[cyan]Failed Questions:[/cyan] ", f"[red]{self.wrongCount}[/red]")
                if self.highScore > 0:
                    t.add_row("[cyan]Highscore:[/cyan] ", f"[yellow]{self.highScore}[/yellow]")
                self.console.log(t)
                if (
                    self.console.input("Replay the game? [cyan](y/n)[/cyan]:").strip().lower()
                    not in self.TRUE_STATEMENTS
                ):
                    self.gameOver = True
                else:
                    self.resetGame()