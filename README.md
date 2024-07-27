If you're unsure of which IDE to use, I recommend vscode.
Unsure of compatibility, but I'm running Python 3.10.6 at the moment and everything is working.

First time setup: 
Enter "source bootstrap.sh" in console.
Then run "flask --app screen_sommelier/screen_sommelier init-db" to initialize flask.

Launching app: 
Enter "flask --app screen_sommelier/screen_sommelier run --debug" in console. Open "http://127.0.0.1:5000" in browser to view the page.

Running tests:
Use command "pytest"

Troubleshooting:
Enter "deactivate" in console to leave virtual environment, then delete venv and rerun first time setup steps.
