phonosemTool

This is a web-application that helps translators to choose only phonosematically expressive Russian translations of English verbs of movement.

Please install node.js, python and optionally git on your machine beforehand.

To download the application on your machine perform these simple stepts:
1. Open powershell and navigate to any folder of your choice;
2. Execute "git clone https://github.com/HandsomeBoulder/phonosemTool.git";
   2.1. Alternatively you can just download a .zip file and unzip it;
4. Execute "cd path_to_folder\phonosemTool";

Configuring backend:
1. Execute "cd path_to_folder\phonosemTool\backend";
2. Create Python virtual environment "python -m venv venv";
3. Activate virtual environmnet ".\venv\Scripts\activate";
4. Install requirements "pip install requirements.txt";
5. Launch API "python api.py";
6. The backend is now running!
N.B. Do not close the PowerShell window! This is not a .service build!

Configuiring frontend:
1. Open another powershell window;
2. Execute "cd path_to_folder\phonosemTool\frontend";
3. Install dependencies "npm install";
4. Launch Quasar "quasar dev";
5. You will now be redirected to the Index page of the application. If you are not redirected, go to "http://localhost:9000/#/".
N.B. Do not close the PowerShell window! This is not a .service build!

The application is fully ready for your input now. Type a verb, a list of verbs or a sentence and test it.
