import requests
import re
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Package Name CLI',
        description='CLI to quickly determine validity of pypi package name')
    parser.add_argument('-n', '--name',
        help="Name you wish to quickly test") 
    invalidURLs = ["requirements", "requirements.txt", "package_name", "<package_name>", "package-name", "<package-name>"]

    name = parser.parse_args().name
    urlToCheck = "https://pypi.org/project/" + name

    pattern = re.compile(r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE)
    if not bool(pattern.match(name)):
        print("Your name does not match the naming conventions. Please see https://packaging.python.org/en/latest/specifications/name-normalization/")
        return

    response = requests.get(urlToCheck)
    if (parser.parse_args().name in invalidURLs):
        print("Invalid pypi package name")
    elif (response.status_code == 404):
        print("Good to go!")
    elif (response.status_code == 200):
        print("Taken pypi package name")
    else:
        print("Status code: " + str(response.status_code))

if __name__ == "__main__":
    main()