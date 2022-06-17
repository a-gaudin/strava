from data_extract.extract import Extract

def main() -> None:
    Extract().update_activities_db()
    print('hello')

if __name__ == "__main__":
    main()