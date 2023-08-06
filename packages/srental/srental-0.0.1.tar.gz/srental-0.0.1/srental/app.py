from srental import create_app

app = create_app()

if __name__ == '__main__':
    """
      Used for local debugging
    """
    app.run(port=8081)
