from flask import (
    render_template, request, Flask, send_from_directory, Blueprint, g)  # Remove: import Flask
import connexion
import user 

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml" )
curr_session = user.session

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
