# name: Nick Martin
# date: 2026/04/02
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5)
#Hot Dog Ratings table

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('HotDogRatings')


def create_hotdog():
    name = input("Enter Hot Dog Type: ").strip()

    if not name:
        print("Hot Dog Type cannot be empty")
        return

    calories_input = input("Enter Calories: ").strip()
    rating_input = input("Enter rating: ").strip()

    try:
        calories = int(calories_input)
        rating = int(rating_input)
    except ValueError:
        print("Calories and rating must be numbers")
        return

    item = {
        "Name": name,
        "Calories": calories,
        "Rating": rating
    }

    table.put_item(Item=item)
    print("Hot Dog created")


def print_hotdog(hotdog):
    name = hotdog.get("Name", "Unknown Name")
    calories = hotdog.get("Calories", "Unknown Calorie Count")
    rating = hotdog.get("Rating", "No Rating")

    print(f"Name: {name}")
    print(f"Calorie Count: {calories}")
    print(f"Rating: {rating}")
    print()


def print_all_hotdogs():
    response = table.scan()
    items = response.get("Items", [])

    print(f"Found {len(items)} hot dog(s):\n")

    for hotdog in items:
        print_hotdog(hotdog)


def update_rating():
    try:
        name = input("Enter hot dog name: ").strip()
        rating = int(input("Enter new rating: ").strip())

        response = table.get_item(Key={"Name": name})
        hotdog = response.get("Item")

        if not hotdog:
            print("Hot dog not found")
            return

        table.update_item(
            Key={"Name": name},
            UpdateExpression="SET Rating = :r",
            ExpressionAttributeValues={":r": rating}
        )

        print("Rating updated")

    except ValueError:
        print("Rating must be a number")
    except Exception as e:
        print(f"Error updating hot dog rating: {e}")


def delete_hotdog():
    name = input("Enter hot dog name: ").strip()

    response = table.get_item(Key={"Name": name})
    hotdog = response.get("Item")

    if not hotdog:
        print("Hot dog not found")
        return

    table.delete_item(Key={"Name": name})
    print("Hot dog deleted")


def query_hotdog():
    name = input("Enter hot dog name: ").strip()

    response = table.get_item(Key={"Name": name})
    hotdog = response.get("Item")

    if not hotdog:
        print("Hot dog not found")
        return

    rating = hotdog.get("Rating")

    if rating is None:
        print("Hot dog has no rating")
        return

    print(f"Rating for {name}: {rating}")


def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new hot dog")
    print("Press R: to READ all hot dogs")
    print("Press U: to UPDATE a hot dog rating")
    print("Press D: to DELETE a hot dog")
    print("Press Q: to QUERY a hot dog's rating")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ").strip()

        if input_char.upper() == "C":
            create_hotdog()
        elif input_char.upper() == "R":
            print_all_hotdogs()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_hotdog()
        elif input_char.upper() == "Q":
            query_hotdog()
        elif input_char.upper() == "X":
            print("Exiting...")
        else:
            print("Not a valid option. Try again.")


main()

