# name: Nick Martin
# date: 2026/04/02
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10, 
# proposed score: 5 (out of 5) 
#Sort function for hotdog dataset

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('HotDogRatings')

def create_hotdog():
    name = input("Enter Hot Dog Type: ").strip()

    if not name:
        print("Hot Dog Type cannot be empty")
        return

    calories_input = input("Enter Calories (or leave blank): ").strip()
    rating_input = input("Enter starting rating (or leave blank): ").strip()

    item = {"Name": name}

    if calories_input:
        try:
            item["Calories"] = int(calories_input)
        except ValueError:
            print("invalid Calorie Count, skipping Calorie coaunt")

    if rating_input:
        try:
            item["Rating"] = [int(rating_input)]
        except ValueError:
            print("invalid rating, using empty ratings list")
            item["Rating"] = []
    else:
        item["Rating"] = []

    table.put_item(Item=item)
    print("Hot Dog created")

def print_hotdog(hotdog):
    name = hotdog.get("Title", "Unknown Title")
    calories = hotdog.get("Calories", "Unknown Calorie count")
    ratings = hotdog.get("Ratings", [])

    print(f"Name: {name}")
    print(f"Calorie Count: {calories}")
    print(f"Ratings: {ratings}")
    print()


def print_all_HotDogs():
    response = table.scan()
    items = response.get("Items", [])

    print(f"Found {len(items)} hot dog(s):\n")

    for hotdog in items:
        print_hotdog(hotdog)

def update_rating():
    try:
        name = input("Enter hot dog name: ").strip()
        rating = int(input("Enter rating: ").strip())

        response = table.get_item(Key={"Name": name})
        hotdog = response.get("Item")

        if not hotdog:
            print("error in updating hot dog rating")
            return

        current_ratings = hotdog.get("Ratings", [])
        current_ratings.append(rating)

        table.update_item(
            Key={"Name": name},
            UpdateExpression="SET Ratings = :r",
            ExpressionAttributeValues={":r": current_ratings}
        )

        print("rating updated")
    except:
        print("error in updating hot dog rating")

def delete_hotdog():
    name = input("Enter hot dog name: ").strip()

    table.delete_item(Key={"Name": name})
    print("hot dog deleted")

def query_hotdog():
    name = input("Enter hot dog name: ").strip()

    response = table.get_item(Key={"Name": name})
    hotdog = response.get("Item")

    if not hotdog:
        print("hot dog not found")
        return

    ratings = hotdog.get("Ratings", [])

    if not ratings:
        print("hot dog has no ratings")
        return

    avg_rating = sum(ratings) / len(ratings)
    print(f"Average rating for {name}: {avg_rating}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new hot dog")
    print("Press R: to READ all hot dogs")
    print("Press U: to UPDATE a hot dog (add a review)")
    print("Press D: to DELETE a hot dog")
    print("Press Q: to QUERY a hot dog's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_hotdog()
        elif input_char.upper() == "R":
            print_all_HotDogs()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_hotdog()
        elif input_char.upper() == "Q":
            query_hotdog()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()

