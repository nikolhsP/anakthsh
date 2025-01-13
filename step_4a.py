# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 17:00:32 2024

@author: User
"""

import json

# Φόρτωση του ανεστραμμένου ευρετηρίου
with open("inverted_index.json", "r", encoding="utf-8") as file:
    inverted_index = json.load(file)

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

# Διεπαφή γραμμής εντολών για τον χρήστη
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
