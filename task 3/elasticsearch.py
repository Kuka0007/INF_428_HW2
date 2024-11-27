import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os
import unittest

ES_INDEX = "threat_scores"
ES_HOST = "http://localhost:9200"
es = Elasticsearch(ES_HOST)

def generate_random_data(mean, variance, num_samples, department_id):
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance, 90)
    threat_scores = np.random.randint(lower_bound, upper_bound + 1, num_samples)
    return [{"department_id": department_id, "threat_score": score} for score in threat_scores]

def save_to_csv(data, filename="threat_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

def load_from_csv(filename="threat_data.csv"):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df.to_dict("records")
    else:
        return []

def populate_elasticsearch(data):
    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(index=ES_INDEX, body={
            "mappings": {
                "properties": {
                    "department_id": {"type": "integer"},
                    "threat_score": {"type": "integer"}
                }
            }
        })
    actions = [
        {"_index": ES_INDEX, "_source": record} for record in data
    ]
    helpers.bulk(es, actions)
    print("Data populated into Elasticsearch.")

def read_from_elasticsearch(department_id):
    query = {
        "query": {
            "match": {
                "department_id": department_id
            }
        }
    }
    results = es.search(index=ES_INDEX, body=query, size=10000)  
    return [hit["_source"]["threat_score"] for hit in results["hits"]["hits"]]

def calculate_department_mean_score(threat_scores):
    return np.mean(threat_scores)

def calculate_aggregated_threat_score(department_scores, department_users):
    weighted_sum = sum(score * users for score, users in zip(department_scores, department_users))
    total_users = sum(department_users)
    return min(max(weighted_sum / total_users, 0), 90)

def generate_and_save_data():
    data = []
    for dept_id in range(1, 6):
        data.extend(generate_random_data(mean=50, variance=10, num_samples=100, department_id=dept_id))
    save_to_csv(data)
    populate_elasticsearch(data)

class TestThreatScoreAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists("threat_data.csv"):
            generate_and_save_data()
    
        # Test Case 1: High score department boosts threat score
    def test_high_score_department(self):
        department_scores = [50, 50, 50, 90, 10]  
        user_counts = [50, 50, 50, 100, 20]     
        
        agg_score = calculate_aggregated_threat_score(department_scores, user_counts)
        
        self.assertTrue(
            agg_score > 50,
            f"Threat score should reflect the influence of the high score department. Got {agg_score}."
        )
    
    # Test Case 2: High variance in one department
    def test_high_variance_department(self):
        department_scores = [50, 50, 50, 50, 90]  
        user_counts = [100, 100, 100, 100, 100]   
        
        agg_score = calculate_aggregated_threat_score(department_scores, user_counts)
        
        self.assertTrue(
            agg_score > 50,
            f"Score should reflect the influence of high-variance departments. Got {agg_score}."
        )
    
    # Test Case 3: All departments have the same scores
    def test_uniform_department_scores(self):
        department_scores = [50, 50, 50, 50, 50]
        user_counts = [100, 100, 100, 100, 100]
        
        agg_score = calculate_aggregated_threat_score(department_scores, user_counts)
        
        self.assertEqual(
            agg_score, 50,
            f"Aggregated score should equal the uniform department score. Got {agg_score}."
        )
    
    # Test Case 4: One department with extreme threats
    def test_extreme_threat_department(self):
        department_scores = [50, 50, 50, 50, 90] 
        user_counts = [100, 100, 100, 100, 500]  
        
        agg_score = calculate_aggregated_threat_score(department_scores, user_counts)
    
        self.assertTrue(
            agg_score > 50,
            f"Aggregated score should be influenced by the extreme threat department. Got {agg_score}."
        )
if __name__ == "__main__":
    unittest.main()
