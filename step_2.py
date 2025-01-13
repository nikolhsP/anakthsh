#Εισαγωγή βιβλιοθηκών
#----------------------------------------------------------------
#Για να διαβάσουμε και να αποθηκεύσουμε δεδομένα σε μορφή JSON
import json
#Η βιβλιοθήκη re είναι για την επεξεργασία κανονικών εκφράσεων
import re
#Η βιβλιοθήκη Natural Language Toolkit (NLTK) χρησιμοποιείται για την επεξεργασία φυσικής γλώσσας
import nltk
#Διάφορα εργαλεία από αυτή τη βιβλιοθήκη
from nltk.corpus import stopwords #Λίστα κοινών λέξεων (όπως "και", "ή", "ο", κ.λπ.) που συνήθως δεν προσφέρουν καμία πληροφορία
from nltk.tokenize import word_tokenize #Χρησιμοποιείται για τον διαχωρισμό ενός κειμένου σε λέξεις
from nltk.stem import PorterStemmer, WordNetLemmatizer #απλοποίηση λέξεων σε μια ριζική μορφή ή σε βασική λέξη

# Λήψη των απαραίτητων εργαλείων του nltk (αν δεν έχουν ήδη κατεβεί)
nltk.download('punkt') 
nltk.download('stopwords') 
nltk.download('wordnet')

# Αρχικοποίηση stop words, stemmer, και lemmatizer
stop_words = set(stopwords.words('english')) #Φτιάχνει ένα σύνολο με τις κοινές αγγλικές λέξεις που θα αγνοηθούν στην επεξεργασία
stemmer = PorterStemmer() #Δημιουργεί ένα αντικείμενο του PorterStemmer για την αφαίρεση της κατάληξης των λέξεων
lemmatizer = WordNetLemmatizer() #Δημιουργεί ένα αντικείμενο του WordNetLemmatizer για την αναγνώριση της βασικής μορφής της λέξης

# Άνοιγμα του JSON αρχείου με τα δεδομένα
with open("output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Λίστα για αποθήκευση των «καθαρισμένων» άρθρων
cleaned_data = []

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

    # Εκτύπωση προόδου κάθε 1 άρθρο
    if (i + 1) % 1 == 0:
        print(f"Επεξεργάστηκαν {i + 1}/{total_articles} άρθρα...")

# Αποθήκευση του καθαρισμένου συνόλου δεδομένων σε νέο JSON αρχείο
output_path = "cleaned_output.json"
with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(cleaned_data, out_file, ensure_ascii=False, indent=2)

print(f"Η προεπεξεργασία ολοκληρώθηκε και τα δεδομένα αποθηκεύτηκαν στο '{output_path}'")
