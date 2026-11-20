
import csv


def load_grades(file_path):

    student_ids = []
    original_grades = []
    rows = []

    with open(file_path, "r", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        headers = reader.fieldnames

        if "ID" not in headers or "Grade" not in headers:
            raise ValueError("CSV must contain ID and Grade columns")

        for row in reader:

            student_id = row["ID"]
            grade = float(row["Grade"])

            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100")

            student_ids.append(student_id)
            original_grades.append(grade)
            rows.append(row)

    if len(student_ids) > 50:
        raise ValueError("Maximum 50 students allowed")

    if len(student_ids) == 0:
        raise ValueError("The CSV file is empty")

    return {
        "file_path": file_path,
        "student_ids": student_ids,
        "original_grades": original_grades,
        "rows": rows,
        "headers": headers
    }


def calculate_grades(original_grades, bonus):

    corrected_grades = []

    for grade in original_grades:

        corrected_grade = grade + bonus

        if corrected_grade > 100:
            corrected_grade = 100

        corrected_grades.append(corrected_grade)

    return corrected_grades


def update_grades_file(filename, student_ids, corrected_grades):

    if len(student_ids) != len(corrected_grades):
        print("Error: Number of grades does not match")
        return

    with open(filename, "w") as f:

        print("ID,Grade", file=f)

        for i in range(len(student_ids)):
            print(student_ids[i], corrected_grades[i], sep=",", file=f)



from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QFileDialog,
    QMessageBox
)

class GradesWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        self.setWindowTitle("Student Grades")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.open_button = QPushButton("Open CSV File")
        layout.addWidget(self.open_button)

        self.open_button.clicked.connect(self.choose_file)


        self.table = QTableWidget()
        self.table.setRowCount(50)
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Original Grades",
            "Corrected Grades"
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_table(self):

        data = load_grades(self.selected_file)

        self.student_ids = data["student_ids"]
        self.original_grades = data["original_grades"]
        self.corrected_grades = data["original_grades"].copy()
        self.selected_file = "grades.csv"

        for i in range(len(self.student_ids)):

            id_item = QTableWidgetItem(
                str(self.student_ids[i])
            )

            original_item = QTableWidgetItem(
                str(self.original_grades[i])
            )

            corrected_item = QTableWidgetItem(
                str(self.corrected_grades[i])
            )

            self.table.setItem(i, 0, id_item)
            self.table.setItem(i, 1, original_item)
            self.table.setItem(i, 2, corrected_item)

    
    def choose_file(self):

        result = QFileDialog.getOpenFileName(
            self,
            "Choose CSV File",
            "",
            "CSV Files (*.csv)"
        )

        filename = result[0]

        if filename != "":
            self.selected_file = filename
            self.load_table()




if __name__ == "__main__":

    app = QApplication([])

    window = GradesWindow()
    window.show()

    app.exec()
