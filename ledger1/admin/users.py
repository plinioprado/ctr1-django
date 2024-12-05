

def get_by_email(user_email: str):
    users = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "pass": "12345",
            "entities": ["example"],
            "entity": "example",
        },
        {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "pass": "12345",
            "entities": ["example"],
            "entity": "example",
        }
    ]

    user = [user for user in users if user["email"] == user_email]

    return {} if user == [] else user[0]

