from extract_entities import extract_from_csv
from build_graph import create_college_graph


def main():
    file_path = "data/college.csv"

    print("Loading College Dataset...")
    triples = extract_from_csv(file_path)

    print("Building Knowledge Graph...")
    create_college_graph(triples)

    print("Graph Generated Successfully!")


if __name__ == "__main__":
    main()