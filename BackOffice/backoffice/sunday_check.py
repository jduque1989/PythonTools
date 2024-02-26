from icecream import ic
import subprocess


def run_script(csv_file):
    ic(subprocess.run(['python', 'cv_team.py', csv_file], check=True))


def main():
    csv_files = ['./teamcv/banco_code.csv', './teamcv/poderosas_code.csv', './teamcv/sona_code.csv']
    for csv_file in csv_files:
        ic(csv_file)
        run_script(csv_file)


if __name__ == "__main__":
    main()
