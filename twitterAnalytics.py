import tweepy
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

## Configuration and authentication of Twitter API

def authenticate_twitter():
    API_KEY = 'XSD8yE83ickuS34I8yQPbNAAj'
    API_SECRET = 'u59e0JT9rZR9UVNMmRHB6VOe6fTqCxBXO56qFYK6IyI'
    ACCESS_TOKEN = '1635001779564716034-VKrsKZVuyQRAiqb0xZufMLM8Yn2Ad2'
    ACCESS_TOKEN_SECRET = 'ruOiUdbJQHryi7PmifYK0tHMta0i7Is0KTyeCQBJxoxBW'
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
return api

Data collection
def collect_followers(api, username):
followers = []
try:
for follower in tweepy.Cursor(api.get_followers, screen_name=username, count=200).items():
followers.append(follower.screen_name)
except tweepy.TweepError as e:
print(f"Error: {e}")
return followers
Network construction
def build_network(api, main_user):
G = nx.DiGraph()
main_followers = collect_followers(api, main_user)
G.add_node(main_user)
G.add_edges_from((main_user, follower) for follower in main_followers)
for follower in main_followers:
followers_of_follower = collect_followers(api, follower)
G.add_edges_from((follower, ff) for ff in followers_of_follower if ff in main_followers) # Limiting connection inside main network
return G
Network analysis
def analyze_network(G):
centrality = nx.degree_centrality(G)
sorted_centrality = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
print("Most influential nodes (Centrality):", sorted_centrality[:5])
return sorted_centrality
Network visualization
def visualize_network(G):
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
plt.show()
Main function
def main():
api = authenticate_twitter()
main_user = input("Enter Twitter username: ")
G = build_network(api, main_user)
analyze_network(G)
visualize_network(G)
if name == "main":
main()
