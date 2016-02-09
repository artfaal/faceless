#Project Faceless.

###Technology: Flask and MongoDB.

For run on local machine:

Install MongoDB

Copy two config files

```
ln -s ?/config.py config.py
mkdir instance
ln -s ?/config_Dev.py instance/config.py
```

Attach static from Y.D.
```
ln -s ?/content app/static/content
```

Load virtualenv and reload Mongo
```
source reload.sh
```

Run Local Server (don't close this window)
```
python run.py
```

Create folder for dump and download it
```
mkdir tmp
fab download_xlsx:l=1 write_to_base:l=1
```

And if we want cool Live Reload (npm requirement):
```
npm install -g browser-sync
browser-sync start --proxy "127.0.0.1:5000" --files "PathToApplicationFolder/app"
```