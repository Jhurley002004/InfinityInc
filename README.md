If you're unsure of which IDE to use, I recommend vscode.
Unsure of compatibility, but I'm running Python 3.10.6 at the moment and everything is working.

First time setup: 
Enter "source bootstrap.sh" in console.
Then run "flask --app screen_sommelier/screen_sommelier init-db" to initialize flask.
Create .env file in parent folder and copy the API key to it. Check Slack for the key or reach out to a team member if you need help.

Launching app: 
Enter "flask --app screen_sommelier/screen_sommelier run --debug" in console. Open "http://127.0.0.1:5000" in browser to view the page.

Running suggestions:
You can try out the suggestions generator by using the command "python screen_sommelier/main/suggestions.py"

Running tests:
Use command "pytest"

Troubleshooting:
Enter "deactivate" in console to leave virtual environment, then delete venv and rerun first time setup steps.
