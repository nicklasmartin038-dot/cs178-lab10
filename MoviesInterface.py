# name: Nick Martin
# date: 2026/04/02
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) 

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    title = input("Enter movie title: ").strip()

    if not title:
        print("movie title cannot be empty")
        return

    year_input = input("Enter year (or leave blank): ").strip()
    rating_input = input("Enter starting rating (or leave blank): ").strip()

    item = {"Title": title}

    if year_input:
        try:
            item["Year"] = int(year_input)
        except ValueError:
            print("invalid year, skipping year")

    if rating_input:
        try:
            item["Ratings"] = [int(rating_input)]
        except ValueError:
            print("invalid rating, using empty ratings list")
            item["Ratings"] = []
    else:
        item["Ratings"] = []

    table.put_item(Item=item)
    print("movie created")

def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", [])
    genre = movie.get("Genre", "Unknown Genre")

    print(f"Title: {title}")
    print(f"Year: {year}")
    print(f"Ratings: {ratings}")
    print(f"Genre: {genre}")
    print()


def print_all_movies():
    response = table.scan()
    items = response.get("Items", [])

    print(f"Found {len(items)} movie(s):\n")

    for movie in items:
        print_movie(movie)

def update_rating():
    try:
        title = input("Enter movie title: ").strip()
        rating = int(input("Enter rating: ").strip())

        response = table.get_item(Key={"Title": title})
        movie = response.get("Item")

        if not movie:
            print("error in updating movie rating")
            return

        current_ratings = movie.get("Ratings", [])
        current_ratings.append(rating)

        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = :r",
            ExpressionAttributeValues={":r": current_ratings}
        )

        print("rating updated")
    except:
        print("error in updating movie rating")

def delete_movie():
    title = input("Enter movie title: ").strip()

    table.delete_item(Key={"Title": title})
    print("movie deleted")

def query_movie():
    title = input("Enter movie title: ").strip()

    response = table.get_item(Key={"Title": title})
    movie = response.get("Item")

    if not movie:
        print("movie not found")
        return

    ratings = movie.get("Ratings", [])

    if not ratings:
        print("movie has no ratings")
        return

    avg_rating = sum(ratings) / len(ratings)
    print(f"Average rating for {title}: {avg_rating}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()

