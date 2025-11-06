import requests

def directory_enumeration(target, wordlist):
    found_directories = []
    with open(wordlist, 'r') as file:
        for line in file:
            directory = line.strip()
            url = f"http://{target/directory}"
            response = requests.get(url)
            if response.status_code == 200:
                found_directories.append(directory)
            else:
                return("Error in directory_enumeration")
            
        return found_directories