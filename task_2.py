import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import concurrent.futures

def download_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Не вдалося завантажити такст з вказаного URL.")
        return None

def clean_text(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    # Видаляємо всі HTML-теги та спеціальні символи
    clean_text = re.sub(r'<.*?>', '', soup.get_text())
    return clean_text

def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

def visualize_top_words(word_counts, top_n=10):
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1])) 
    top_words = list(sorted_word_counts.keys())[-top_n:] 
    counts = [sorted_word_counts[word] for word in top_words]
    
    plt.figure(figsize=(10, 6))
    plt.barh(top_words, counts, color='skyblue') 
    plt.xlabel('Frequency') 
    plt.ylabel('Words') 
    plt.title('Top {} Words in the Text'.format(top_n))
    plt.tight_layout()
    plt.show()

def main():
    while True:
        url = input("Вкажіть URL, щоб завантажити текст (або 'exit' для виходу): ")
        if url.lower() == 'exit':
            break
        
        html_text = download_text(url)
        if html_text:
            text = clean_text(html_text)
            
            # Використання багатопотоковості для виконання map_reduce
            with concurrent.futures.ThreadPoolExecutor() as executor:
                word_counts = executor.submit(map_reduce, text).result()
            
            print("Результат підрахунку слів:", word_counts)
            visualize_top_words(word_counts)

if __name__ == "__main__":
    main()

# Example usage: 
# https://teacheng.info/reading/fairy-tales/