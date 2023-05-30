1. git clone this project
2. in pycharm: add venv in config: ctrl+alt+s 
   1. Project: immo-kleinanzeigen
   2. Python interpreter
   3. add new interpreter
   4. Virtualenv interpreter
3. go into Terminal (in pycharm), make sure you are in root dir (entering "dir" will show you scrapy.cfg file)
4. enter `scrapy crawl kleinanzeigen -o result.csv`