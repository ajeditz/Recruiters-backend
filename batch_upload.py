import requests

API_URL = "http://localhost:8000/recruiters/"
recruiters_data = [
    {
        "profile_picture_url": "https://example.com/recruiter1.jpg",
        "recruiter_name": "Alice Johnson",
        "recruiter_rating": 4,
        "location": "New York, USA",
        "verified_badge": True,
        "num_candidates_listed": 25,
        "tags": ["Hospitality Manager", "Executive Chef"],
        "bio": "Specializes in placing top-tier hospitality managers.",
        "successful_deals": 150
    },
    {
        "profile_picture_url": "https://example.com/recruiter2.jpg",
        "recruiter_name": "John Smith",
        "recruiter_rating": 3,
        "location": "London, UK",
        "verified_badge": True,
        "num_candidates_listed": 18,
        "tags": ["Sous Chef", "Event Manager"],
        "bio": "Expert in matching culinary talent with elite establishments.",
        "successful_deals": 120
    },
    {
        "profile_picture_url": "https://example.com/recruiter3.jpg",
        "recruiter_name": "Sophia Brown",
        "recruiter_rating": 5,
        "location": "Dubai, UAE",
        "verified_badge": False,
        "num_candidates_listed": 30,
        "tags": ["Hotel Manager", "Food & Beverage Manager"],
        "bio": "Known for connecting luxury hotel executives with the best opportunities.",
        "successful_deals": 200
    },
    {
        "profile_picture_url": "https://example.com/recruiter4.jpg",
        "recruiter_name": "Michael Lee",
        "recruiter_rating": 4,
        "location": "Singapore",
        "verified_badge": True,
        "num_candidates_listed": 22,
        "tags": ["Front Desk Executive", "Event Coordinator"],
        "bio": "Passionate about streamlining front-of-house talent placement.",
        "successful_deals": 180
    },
    {
        "profile_picture_url": "https://example.com/recruiter5.jpg",
        "recruiter_name": "Emma Davis",
        "recruiter_rating": 2,
        "location": "Paris, France",
        "verified_badge": False,
        "num_candidates_listed": 19,
        "tags": ["Concierge", "Hospitality Trainer"],
        "bio": "Focuses on high-end hospitality roles in Europe.",
        "successful_deals": 130
    },
    {
        "profile_picture_url": "https://example.com/recruiter6.jpg",
        "recruiter_name": "Liam White",
        "recruiter_rating": 4,
        "location": "Toronto, Canada",
        "verified_badge": True,
        "num_candidates_listed": 28,
        "tags": ["Banquet Manager", "Executive Assistant"],
        "bio": "Trusted by top-tier clients for executive placements.",
        "successful_deals": 160
    },
    {
        "profile_picture_url": "https://example.com/recruiter7.jpg",
        "recruiter_name": "Olivia Martinez",
        "recruiter_rating": 3,
        "location": "Barcelona, Spain",
        "verified_badge": True,
        "num_candidates_listed": 20,
        "tags": ["Restaurant Manager", "Housekeeping Supervisor"],
        "bio": "Excels in finding talent for boutique hotels and restaurants.",
        "successful_deals": 140
    },
    {
        "profile_picture_url": "https://example.com/recruiter8.jpg",
        "recruiter_name": "Noah Wilson",
        "recruiter_rating": 3,
        "location": "Berlin, Germany",
        "verified_badge": False,
        "num_candidates_listed": 21,
        "tags": ["Spa Manager", "Bar Manager"],
        "bio": "Specialized in wellness and entertainment talent.",
        "successful_deals": 110
    },
    {
        "profile_picture_url": "https://example.com/recruiter9.jpg",
        "recruiter_name": "Ava Taylor",
        "recruiter_rating": 4,
        "location": "Mumbai, India",
        "verified_badge": True,
        "num_candidates_listed": 27,
        "tags": ["Event Planner", "Hospitality Consultant"],
        "bio": "India's top recruiter for event and consultancy roles.",
        "successful_deals": 210
    },
    {
        "profile_picture_url": "https://example.com/recruiter10.jpg",
        "recruiter_name": "William Brown",
        "recruiter_rating": 5,
        "location": "Sydney, Australia",
        "verified_badge": True,
        "num_candidates_listed": 15,
        "tags": ["Catering Manager", "Hotel Supervisor"],
        "bio": "Connecting top talents to Australia's best venues.",
        "successful_deals": 100
    },
    {
        "profile_picture_url": "https://example.com/recruiter11.jpg",
        "recruiter_name": "Mia Clark",
        "recruiter_rating": 3,
        "location": "Bangkok, Thailand",
        "verified_badge": False,
        "num_candidates_listed": 16,
        "tags": ["Travel Consultant", "Reservation Manager"],
        "bio": "Expert in travel and hospitality recruitment.",
        "successful_deals": 90
    },
    {
        "profile_picture_url": "https://example.com/recruiter12.jpg",
        "recruiter_name": "Elijah Hall",
        "recruiter_rating": 5,
        "location": "Rome, Italy",
        "verified_badge": True,
        "num_candidates_listed": 18,
        "tags": ["Chef de Cuisine", "Pastry Chef"],
        "bio": "Bringing Italy's culinary talent to international kitchens.",
        "successful_deals": 170
    },
    {
        "profile_picture_url": "https://example.com/recruiter13.jpg",
        "recruiter_name": "Charlotte Moore",
        "recruiter_rating": 5,
        "location": "Cape Town, South Africa",
        "verified_badge": False,
        "num_candidates_listed": 14,
        "tags": ["Hospitality Analyst", "Executive Coordinator"],
        "bio": "Focused on high-level hospitality roles in Africa.",
        "successful_deals": 80
    }
]


def batch_upload_recruiters(api_url, recruiters):
    for recruiter in recruiters:
        response = requests.post(api_url, json=recruiter)
        if response.status_code == 201:
            print(f"Successfully added recruiter: {recruiter['recruiter_name']}")
        else:
            print(f"Failed to add recruiter: {recruiter['recruiter_name']} - {response.text}")

if __name__ == "__main__":
    batch_upload_recruiters(API_URL, recruiters_data)
