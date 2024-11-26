from elasticsearch import Elasticsearch
import json

es = Elasticsearch("http://localhost:9200")

index_name = "billionaires"

def get_top_billionaires():
    query = {
        "size": 10,
        "sort": [{"finalWorth": {"order": "desc"}}], 
        "_source": ["personName", "finalWorth", "rank", "country"] 
    }
    
    response = es.search(index=index_name, body=query)
    return response['hits']['hits']

def calculate_threat_scores(billionaires):
    threat_scores = {}
    for billionaire in billionaires:
        person_name = billionaire['_source']['personName']
        final_worth = billionaire['_source']['finalWorth']
        
        threat_score = final_worth / 10
        if final_worth > 100000:  
            threat_score *= 2 
        
        threat_scores[person_name] = threat_score
    
    return threat_scores

top_billionaires = get_top_billionaires()

threat_scores = calculate_threat_scores(top_billionaires)

print("Top 10 billionaires and their threat scores:")
for person_name, score in threat_scores.items():
    print(f"{person_name}: Threat Score = {score}")

