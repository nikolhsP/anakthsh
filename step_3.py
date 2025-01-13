import json
import re
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Λήψη των απαραίτητων εργαλείων του nltk (αν δεν έχουν ήδη κατεβεί)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Αρχικοποίηση stop words, stemmer, και lemmatizer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Άνοιγμα του JSON αρχείου με τα δεδομένα
with open("./output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Λίστα για αποθήκευση των «καθαρισμένων» άρθρων
cleaned_data = []

# Δημιουργία ευρετηρίου (Inverted Index)
inverted_index = {}

# Συνολικός αριθμός άρθρων
total_articles = len(data)
print(f"Συνολικός αριθμός άρθρων προς επεξεργασία: {total_articles}")

# Καθαρισμός και προεπεξεργασία κειμένου για κάθε άρθρο
for i, article in enumerate(data[:3]): #Διαβαζει μονο τα πρωτα 3 αρθρα
    title = article.get("title", "")
    text = article.get("text", "")

    # 1. Κανονικοποίηση (μετατροπή σε πεζά)
    text = text.lower()

    # 2. Tokenization (Διαχωρισμός του κειμένου σε λέξεις)
    tokens = word_tokenize(text)

    # 3. Αφαίρεση σημείων στίξης και stop words
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    # Επιβεβαίωση ότι έχουν αφαιρεθεί τα stop words
    filtered_tokens = [word for word in tokens if word in stop_words]
    if filtered_tokens:
        print(f"Προσοχή: Τα παρακάτω stop words δεν αφαιρέθηκαν: {filtered_tokens}")

    # 4. Stemming ή Lemmatization
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # 5. Επανασύνθεση των tokens σε καθαρισμένο κείμενο
    cleaned_text = ' '.join(lemmatized_tokens)

    # Προσθήκη στο νέο σύνολο δεδομένων
    cleaned_article = {
        "title": title,
        "cleaned_text": cleaned_text
    }
    cleaned_data.append(cleaned_article)

    # Αναγνώριση των λέξεων (tokens)
    for word in set(lemmatized_tokens):  # Χρησιμοποιούμε set για να μην προσθέσουμε την ίδια λέξη πολλές φορές
        if word not in inverted_index:
            inverted_index[word] = []
        inverted_index[word].append(i)  # Αποθηκεύουμε τον αριθμό του άρθρου (index)

    # Εκτύπωση προόδου κάθε 1 άρθρο
    if (i + 1) % 1 == 0:
        print(f"Επεξεργάστηκαν {i + 1}/{total_articles} άρθρα...")

# Αποθήκευση του καθαρισμένου συνόλου δεδομένων σε νέο JSON αρχείο
output_path = "cleaned_output.json"
with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(cleaned_data, out_file, ensure_ascii=False, indent=2)

print(f"Η προεπεξεργασία ολοκληρώθηκε και τα δεδομένα αποθηκεύτηκαν στο '{output_path}'")

# Αποθήκευση του ευρετηρίου (Inverted Index)
index_output_path = "inverted_index.json"
with open(index_output_path, "w", encoding="utf-8") as index_file:
    json.dump(inverted_index, index_file, ensure_ascii=False, indent=2)

print(f"Το ευρετήριο αποθηκεύτηκε στο '{index_output_path}'")

