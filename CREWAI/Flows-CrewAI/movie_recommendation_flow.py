# from crewai.flow.flow import Flow, start, listen
# from crewai import Agent, Task
# import openai
# import os

# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# class MovieRecommendationFlow(Flow):

#     def __init__(self):
#         super().__init__()


#     @start
#     def generate_genre(self):
#         response = openai_client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "user", "content": "Give me a random movie genre."}
#             ]
#         )
#         print("Generated Genre Response:", response)
#         return response.choices[0].message["content"].strip()
    
#     @listen(generate_genre)
#     def recommend_movie(self, genre: str):
#         response = openai_client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "user", "content": f"Recommend a movie in the {genre} genre."}
#             ]
#         )
#         movie_recommendation = response.choices[0].message.content.strip()
#         print(f"Genre: {genre}")
#         print(f"Recommended Movie: {movie_recommendation}")
#         return movie_recommendation

import ollama
from crewai.flow.flow import Flow, listen, start
from models.structured_flow import StructuredFlow

class MovieRecommendationFlow(Flow[StructuredFlow]):

    @start()
    def generate_genre(self):

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": "Give me a random movie genre.",
                },
            ],
        )

        random_genre = response.message.content
        print(f"Flow started. State ID: {self.state.id}")
        self.state.task = "Develop a new API endpoint"
        self.state.status = "Pending"
        self.state.genre = random_genre
        print(f"Task generated: {self.state.task} (Status: {self.state.status})")

        return random_genre
    
    @listen(generate_genre)
    def recommend_movie(self, random_genre):
    
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": f"Recommend a movie in the {random_genre} genre.",
                },
            ],
        )

        movie_recommendation = response.message.content
        self.state.status = "In Progress"
        print(f"Task status updated: {self.state.status}")
        self.state.recommendation = movie_recommendation
        return movie_recommendation
    
    @listen(recommend_movie)
    def complete_task(self):
        self.state.status = "Completed"
        print(f"Task status updated: {self.state.status}")
        print(f"Final Task State: {self.state}")