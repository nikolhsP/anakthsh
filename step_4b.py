import json
import math
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Φόρτωση του ανεστραμμένου ευρετηρίου
with open("inverted_index.json", "r", encoding="utf-8") as file:
    inverted_index = json.load(file)

# Συνάρτηση για την ανάκτηση εγγράφων βάσει όρου
def get_documents(term):
    return set(inverted_index.get(term, []))

# Συνάρτηση για την επεξεργασία ερωτήματος
def process_query(query):
    tokens = query.split()
    stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i].lower()
        if token == "and":
            operand1 = stack.pop()
            operand2 = get_documents(tokens[i + 1])
            stack.append(operand1 & operand2)
            i += 1
        elif token == "or":
            operand1 = stack.pop()
            operand2 = get_documents(tokens[i + 1])
            stack.append(operand1 | operand2)
            i += 1
        elif token == "not":
            operand2 = get_documents(tokens[i + 1])
            stack.append(set(range(len(inverted_index))) - operand2)
            i += 1
        else:
            stack.append(get_documents(token))
        i += 1
    return stack.pop()

# Συνάρτηση TF-IDF για την κατάταξη αποτελεσμάτων
def compute_tfidf(query, documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    
    similarities = np.dot(query_vector, tfidf_matrix.T).toarray().flatten()
    return similarities

# Συνάρτηση για τον υπολογισμό της BM25
def compute_bm25(query, documents, k1=1.5, b=0.75):
    avg_doc_len = np.mean([len(doc.split()) for doc in documents])
    idf = defaultdict(lambda: 0)
    doc_len = [len(doc.split()) for doc in documents]
    
    for doc in documents:
        for term in doc.split():
            idf[term] += 1
    
    idf = {term: math.log((len(documents) - freq + 0.5) / (freq + 0.5) + 1.0) for term, freq in idf.items()}
    
    scores = []
    for doc, length in zip(documents, doc_len):
        score = 0
        for term in query.split():
            term_freq = doc.split().count(term)
            score += idf.get(term, 0) * (term_freq * (k1 + 1)) / (term_freq + k1 * (1 - b + b * length / avg_doc_len))
        scores.append(score)
    
    return scores

# Συνάρτηση για την ταξινόμηση αποτελεσμάτων
def rank_documents(query, documents, ranking_algorithm="boolean"):
    if ranking_algorithm == "boolean":
        # Αναζήτηση με Boolean
        result = process_query(query)
        return sorted(result)
    elif ranking_algorithm == "tfidf":
        # TF-IDF Ranking
        similarities = compute_tfidf(query, documents)
        ranked_docs = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in ranked_docs]
    elif ranking_algorithm == "bm25":
        # BM25 Ranking
        scores = compute_bm25(query, documents)
        ranked_docs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in ranked_docs]

# Διεπαφή γραμμής εντολών για τον χρήστη
def main():
    print("Καλωσορίσατε στη Μηχανή Αναζήτησης!")
    print("\nΜπορείτε να χρησιμοποιήσετε τους παρακάτω τελεστές για τη σύνθεση των ερωτημάτων σας:")
    print("- OR: Επιστρέφει έγγραφα που περιέχουν οποιονδήποτε από τους όρους (π.χ. 'machine OR learning').")
    print("- AND: Επιστρέφει έγγραφα που περιέχουν όλους τους όρους (π.χ. 'machine AND learning').")
    print("- NOT: Εξαιρεί έγγραφα που περιέχουν τον όρο (π.χ. 'NOT neural').")
    
    # Λίστα εγγράφων για δοκιμή
    documents = [
        "This is a document about machine learning.",
        "This document is about neural networks and deep learning.",
        "Another document about machine learning applications."
    ]
    
    while True:
        print("\nΕπιλέξτε τον αλγόριθμο κατάταξης:")
        print("1: Boolean Retrieval")
        print("2: TF-IDF Ranking")
        print("3: Okapi BM25")
        print("Πληκτρολογήστε 'q' για έξοδο.")
        
        choice = input("Επιλογή αλγορίθμου (1/2/3): ").strip()
        if choice.lower() == "q":
            print("Αντίο! Σας ευχαριστούμε που χρησιμοποιήσατε τη Μηχανή Αναζήτησης.")
            break

        # Επιλογή αλγορίθμου κατάταξης
        if choice == "1":
            ranking_algorithm = "boolean"
        elif choice == "2":
            ranking_algorithm = "tfidf"
        elif choice == "3":
            ranking_algorithm = "bm25"
        else:
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
            continue

        # Εισαγωγή ερωτήματος
        print("\nΕισάγετε το ερώτημά σας για αναζήτηση:")
        query = input("Πληκτρολογήστε 'q' για έξοδο.\n> ").strip()
        if query.lower() == "q":
            print("Αντίο! Σας ευχαριστούμε που χρησιμοποιήσατε τη Μηχανή Αναζήτησης.")
            break

        try:
            # Κατάταξη και εμφάνιση αποτελεσμάτων
            ranked_docs = rank_documents(query, documents, ranking_algorithm)
            if ranked_docs:
                print(f"\nΒρέθηκαν {len(ranked_docs)} σχετικά έγγραφα: {ranked_docs}")
            else:
                print("\nΔεν βρέθηκαν σχετικά έγγραφα.")
        except Exception as e:
            print(f"\nΣφάλμα κατά την επεξεργασία του ερωτήματος: {e}")

if __name__ == "__main__":
    main()
