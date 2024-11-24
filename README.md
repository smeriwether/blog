## Blog

A small Flask app with a SQLite backend.

### Deploying to a server

On the build machine:

1. Build the blog with `python -m build --wheel`
2. Move the wheel file to the host machine

On the host machine:

1. Create a virtual environment with `python -m venv .venv`
2. Activate the virtual environment with `. .venv/bin/activate`
3. Install the wheel with `pip install blog-1.0.0-py3-none-any.whl` (or whatever the new version is)
4. Create the database with `flask --app blog init-db`
5. Configure the secret key by:
   - Creating a new key with `python -c 'import secrets; print(secrets.token_hex())'`
   - Creating a `config.py` file with `touch .venv/var/blog-isntance/config.py`
   - Copy the created key into `config.py` with the format `SECRET_KEY = "<key>"`
6. Install waitress as the production server with `pip install waitress`
7. Serve the blog through waitress with `waitress-serve --call 'blog:create_app`

### Deploy to a RaspberryPi

I deployed the blog to my RaspberryPi using the steps above with slight modifications. On Step 7, I used the command
`waitress-serve --call 'blog:create_app &` to run the command in the background (notice the `&`).

I use Tailscale on the RaspberryPi and every blog "client" to create a secure tunnel to the blog. In other words, the
RaspberryPi, and my blog, are not exposed to the internet.

### Backing up the RaspberryPi

The SQLite database is stored as a file inside the blog's virtual environment (located at `.venv/var/blog_instance/blog.sqlite`).
I back up that database to an external drive so I don't lose any history of what I've written. I created a Samba Server to expose
the database to my Mac Mini. Once it's discoverable from my Mac Mini I use Carbon Copy Cloner to backup those files to an external disk and my NAS.
Here's how I did that:

1. Create a new folder on the RaspberryPi called `Servers`
2. Move (or install) the blog to the `Servers` folder
3. Install Samba with `sudo apt install samba samba-common-bin`
4. Open the smb.conf file with `sudo vim /etc/samba/smb.conf`
5. Add the following to the bottom of the file:

```
[piservers]
path = /home/srm/Servers
writeable = yes
browseable = yes
public=no
```

6. Create a username and password with `sudo smbpasswd -a <USERNAME>`
   - Enter a password when prompted
7. Restart Samba with `sudo systemctl restart smbd`

This makes the `Servers` folder discoverable from my Mac Mini.
