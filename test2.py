import json

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

# Συνάρτηση για την υπολογισμό ακρίβειας, ανάκλησης, F1-Score και MAP
def evaluate_search_system(queries, relevant_docs):
    precision_scores = []
    recall_scores = []
    f1_scores = []
    map_scores = []
    
    for query, relevant_set in zip(queries, relevant_docs):
        retrieved_docs = process_query(query)
        
        # Ακρίβεια (Precision)
        precision = len(retrieved_docs & relevant_set) / len(retrieved_docs) if retrieved_docs else 0
        precision_scores.append(precision)
        
        # Ανάκληση (Recall)
        recall = len(retrieved_docs & relevant_set) / len(relevant_set) if relevant_set else 0
        recall_scores.append(recall)
        
        # F1-Score
        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0
        f1_scores.append(f1)
        
        # Μέση Ακρίβεια (MAP)
        total_retrieved = len(retrieved_docs)
        avg_precision = 0
        count = 0
        for doc in retrieved_docs:
            count += 1
            if doc in relevant_set:
                avg_precision += count / total_retrieved
        map_scores.append(avg_precision / len(relevant_set) if relevant_set else 0)
    
    # Υπολογισμός Μέσου Όρου
    avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0
    avg_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0
    avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0
    avg_map = sum(map_scores) / len(map_scores) if map_scores else 0
    
    return avg_precision, avg_recall, avg_f1, avg_map

# Παράδειγμα ερωτημάτων και σχετικών εγγράφων
queries = [
    "machine learning",
    "deep learning",
    "natural language processing"
]

relevant_docs = [
    {0, 2, 3},  # Σχετικά έγγραφα για το πρώτο ερώτημα
    {1, 4},      # Σχετικά έγγραφα για το δεύτερο ερώτημα
    {0, 3}       # Σχετικά έγγραφα για το τρίτο ερώτημα
]

# Αξιολόγηση του συστήματος
precision, recall, f1, map_score = evaluate_search_system(queries, relevant_docs)

# Εμφάνιση αποτελεσμάτων
print(f"Ακρίβεια: {precision}")
print(f"Ανάκληση: {recall}")
print(f"F1-Score: {f1}")
print(f"Μέση Ακρίβεια (MAP): {map_score}")
