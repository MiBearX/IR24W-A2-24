
def run(filepath: str) -> None:
    with open(filepath, 'r') as the_file:
        for line in the_file:
            print('\"' + line.strip() + '\"' + ",", end = "")

if __name__ == '__main__':
    run(input("Enter name of file"))