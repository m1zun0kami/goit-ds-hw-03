from pymongo import MongoClient
from config import MONGO_URL


client = MongoClient(MONGO_URL)


db = client['cats']
collection = db['cats']

def insert_cats():
    """
    Insert initial cat documents into the collection.
    """
    cat_one = collection.insert_one(
        {
            'name': 'barsik',
            'age': 3,
            'features': ['feature_1', 'feature_2', 'feature_3'],
        }
    )
    print(cat_one.inserted_id)


    cat_many = collection.insert_many(
        [
            {
                'name': 'Stepan',
                'age': 2,
                'features': ['feature_2', 'feature_4', 'feature_5'],
            },
            {
                'name': 'Lana',
                'age': 4,
                'features': ['feature_3', 'feature_5', 'feature_6'],
            }
        ]
    )
    print(cat_many.inserted_ids)


def read_all():
    """
    Print all cat documents from the collection.
    """
    try:
        for cat in collection.find():
            print(cat)
    except Exception as e:
        print(f'Error: {e}')


def find_cat():
    """
    Ask for a cat's name and print the matching document, if it exists.
    """
    try:
        name = input("Please input cat's name:")
        cat = collection.find_one({'name': name})
        if cat:
            print(cat)
        else:
            print('Cat not found error')
    except Exception as e:
        print(f'Error: {e}')


def update_cat():
    """
    Ask for a cat's name and a new age, then update the cat's age.
    """
    try:
        name = input("Please input cat's name:")
        new_age = int(input("Please input updated age:"))
        update = collection.update_one({'name': name}, {'$set': {'age': new_age}})
        if update.matched_count:
            print('Updated successfully')
        else:
            print('Cat not found error')
    except ValueError:
        print('Age must be a whole number')
        update_cat()
    except Exception as e:
        print(f'Error: {e}')


def update_feature():
    """
    Ask for a cat's name and a feature, then add the feature to the cat's list (no duplicates).
    """
    try:
        name = input("Please input cat's name:")
        new_feature = input('Please input a new feature:')
        update = collection.update_one({'name': name}, {'$addToSet': {'features': new_feature}})
        if update.matched_count:
            print('Feature added')
        else:
            print('Cat not found error')
    except Exception as e:
        print(f'Error: {e}')


def delete_cat():
    """
    Ask for a cat's name and delete the matching document.
    """
    try:
        name = input("Please input cat's name:")
        deletion = collection.delete_one({'name': name})
        if deletion.deleted_count:
            print('Deleted successfully')
        else:
            print('Cat not found error')
    except Exception as e:
        print(f'Error: {e}')


def delete_cats():
    """
    Delete all cats from the collection after user confirmation (y/n).
    """
    try:
        confirm = input('Are you sure you want to delete all cats? (y/n)').lower()
        if confirm == 'y':
            deletion = collection.delete_many({})
            if deletion.deleted_count:
                print('Deleted successfully')
            else:
                print('Cats not found error')
        elif confirm == 'n':
            print('Deletion cancelled')
        else:
            print("Please answer 'y' to confirm or 'n' to cancel")
            delete_cats()
    except Exception as e:
        print(f'Error: {e}')


def main():
    """
    Run the command loop and call the matching function for each command.
    """
    while True:
        user_input = input(
            "enter a command:\n"
            "insert_cats - populate collection;\n"
            "read_all - show all cats;\n"
            "find_cat - find cat by name;\n"
            "update_cat - update cat's age by name;\n"
            "update_feature - add new feature by name;\n"
            "delete_cat - delete cat by name;\n"
            "delete_cats - delete all cats;\n"
            "exit - stop program.\n"
            ">"
        ).lower().strip()

        if user_input == 'exit':
            break

        elif user_input == 'insert_cats':
            insert_cats()

        elif user_input == 'read_all':
            read_all()

        elif user_input == 'find_cat':
            find_cat()

        elif user_input == 'update_cat':
            update_cat()

        elif user_input == 'update_feature':
            update_feature()

        elif user_input == 'delete_cat':
            delete_cat()

        elif user_input == 'delete_cats':
            delete_cats()

        else:
            print('invalid command')


if __name__ == '__main__':
    main()