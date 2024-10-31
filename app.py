from flask import Flask, request, jsonify
from twitter_api import TwitterAPI
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Charge env vars
load_dotenv()

# Initialize twitter API
twitter_api = TwitterAPI()

app = Flask(__name__)

#Def for get unique stats of a user
@app.route('/get_user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    if not username:
        return jsonify({"error": "Username is required"}), 400

   #Get Dates by the user
    user_data = twitter_api.get_user_by_username(username)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "Could not retrieve user data"}), 500

@app.route('/get_me', methods=['GET'])
def get_me():
    # Get Dates for the authentiqued user
    user_data = twitter_api.get_authenticated_user()
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "Could not retrieve authenticated user data"}), 500

@app.route('/compare_users', methods=['GET'])
def compare_users():
    username1 = request.args.get('username1')
    username2 = request.args.get('username2')

    if not username1 or not username2:
        return jsonify({"error": "Both usernames are required"}), 400

    # Get Data for both users
    user_data1 = twitter_api.get_user_by_username(username1)
    user_data2 = twitter_api.get_user_by_username(username2)

    if user_data1 and user_data2:
        # Send data to get a graph
        plot_user_comparison(user_data1, user_data2)
        return jsonify({"message": "Graph created successfully!"}), 200
    else:
        return jsonify({"error": "Could not retrieve data for both users"}), 500

def plot_user_comparison(user_data1, user_data2):
    # Extract Metrics
    metrics1 = user_data1.get("public_metrics", {})
    metrics2 = user_data2.get("public_metrics", {})

    # Definie tags
    labels = ["Followers", "Following", "Tweets", "Listed"]
    # Extract metrics
    values1 = [
        metrics1.get("followers_count", 0),
        metrics1.get("following_count", 0),
        metrics1.get("tweet_count", 0),
        metrics1.get("listed_count", 0)
    ]
    values2 = [
        metrics2.get("followers_count", 0),
        metrics2.get("following_count", 0),
        metrics2.get("tweet_count", 0),
        metrics2.get("listed_count", 0)
    ]

    #Normalize data
    normalized_values1 = []
    normalized_values2 = []

    for i in range(len(labels)):
        max_value = max(values1[i], values2[i])  # Max Value for the metric
        if max_value > 0:
            normalized_values1.append((values1[i] / max_value) * 100)
            normalized_values2.append((values2[i] / max_value) * 100)
        else:
            # if max value is 0 both get 0
            normalized_values1.append(0)
            normalized_values2.append(0)

    # Configure graph
    x = range(len(labels))
    plt.figure(figsize=(10, 6))
    plt.bar(x, normalized_values1, width=0.4, label=user_data1.get("username"), color='b', align='center')
    plt.bar([p + 0.4 for p in x], normalized_values2, width=0.4, label=user_data2.get("username"), color='g', align='center')

    # Configure tags and metrics
    plt.xlabel("Metrics")
    plt.ylabel("Normalized Percentage (%)")
    plt.title("Comparison of User Metrics (Independently Normalized)")
    plt.xticks([p + 0.2 for p in x], labels)
    plt.legend()

    # save as a image
    plt.savefig("user_comparison.png")
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
