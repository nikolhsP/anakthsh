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

# Συνάρτηση για την ανάκτηση εγγράφων βάσει όρου
def get_documents(term):
    return set(inverted_index.get(term, []))

# Συνάρτηση για την επεξεργασία ερωτήματος
def process_query(query):
    # Διάσπαση του ερωτήματος σε tokens
    tokens = query.split()

    # Στοίβα για διαχείριση Boolean τελεστών
    stack = []

    # Διαχείριση Boolean τελεστών
    i = 0
    while i < len(tokens):
        token = tokens[i].lower()

        if token == "and":
            # Λειτουργία AND
            operand1 = stack.pop()
            operand2 = get_documents(tokens[i + 1])
            stack.append(operand1 & operand2)
            i += 1
        elif token == "or":
            # Λειτουργία OR
            operand1 = stack.pop()
            operand2 = get_documents(tokens[i + 1])
            stack.append(operand1 | operand2)
            i += 1
        elif token == "not":
            # Λειτουργία NOT
            operand2 = get_documents(tokens[i + 1])
            stack.append(set(range(len(inverted_index))) - operand2)
            i += 1
        else:
            # Επεξεργασία όρου
            stack.append(get_documents(token))
        i += 1

    # Το τελευταίο στοιχείο στη στοίβα είναι το αποτέλεσμα
    return stack.pop()

# Ρώτα το χρήστη αν θέλει να αναζητήσει κάτι στο ευρετήριο
def ask_user_for_search():
    user_input = input("Θέλεις να αναζητήσεις κάτι στο ευρετήριο (y/n)? ").strip().lower()
    
    if user_input == 'y':
        start_search()
    elif user_input == 'n':
        print("Bye!")
    else:
        print("Μη έγκυρη επιλογή. Παρακαλώ εισάγετε 'y' ή 'n'.")
        ask_user_for_search()

# Διεπαφή γραμμής εντολών για τον χρήστη
def start_search():
    print("Καλωσορίσατε στη Μηχανή Αναζήτησης!")
    print("\nΜπορείτε να χρησιμοποιήσετε τους παρακάτω τελεστές για τη σύνθεση των ερωτημάτων σας:")
    print("- OR: Επιστρέφει έγγραφα που περιέχουν οποιονδήποτε από τους όρους (π.χ. 'machine OR learning').")
    print("- AND: Επιστρέφει έγγραφα που περιέχουν όλους τους όρους (π.χ. 'machine AND learning').")
    print("- NOT: Εξαιρεί έγγραφα που περιέχουν τον όρο (π.χ. 'NOT neural').")

    while True:
        print("\nΕισάγετε το ερώτημά σας για αναζήτηση:")
        query = input("Πληκτρολογήστε 'q' για έξοδο.\n> ").strip()
        if query.lower() == "q":
            print("Αντίο! Σας ευχαριστούμε που χρησιμοποιήσατε τη Μηχανή Αναζήτησης.")
            break

        try:
            # Επεξεργασία του ερωτήματος
            result = process_query(query)

            # Εμφάνιση αποτελεσμάτων
            if result:
                print(f"\nΒρέθηκαν {len(result)} σχετικά έγγραφα: {sorted(result)}")
            else:
                print("\nΔεν βρέθηκαν σχετικά έγγραφα.")
        except Exception as e:
            print(f"\nΣφάλμα κατά την επεξεργασία του ερωτήματος: {e}")





            

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

# Ξεκινάμε τη διαδικασία με την ερώτηση στο χρήστη
ask_user_for_search()

