def learn_commit(author: str, message: str):
    try:
        text = f"{author}: {message}"
        vector = get_embedding(text)

        data = {
            "author": author,
            "message": message
        }

        add(vector, data)

    except Exception as e:
        print("Learn failed:", e)
