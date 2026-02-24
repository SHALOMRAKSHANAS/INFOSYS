import csv

def extract_from_csv(file_path):
    triples = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student = row["Student"]
            course = row["Course"]
            professor = row["Professor"]
            department = row["Department"]
            college = row["College"]

            triples.extend([
                (student, "enrolled_in", course, "Student", "Course"),
                (course, "taught_by", professor, "Course", "Professor"),
                (professor, "belongs_to", department, "Professor", "Department"),
                (department, "part_of", college, "Department", "College"),
            ])

    return triples