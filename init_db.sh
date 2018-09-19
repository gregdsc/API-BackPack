#!/bin/sh
sudo -u postgres createdb backpack-local
if ["$SHELL" == "/bin/bash"]
then
    echo "export DATABASE_URL=\"postgres://postgres:postgres@localhost/backpack-local\"" >> ~/.bashrc
    export DATABASE_URL="postgres://postgres:postgres@localhost/backpack-local"
else
    echo "export DATABASE_URL=\"postgres://postgres:postgres@localhost/backpack-local\"" >> ~/.zshrc
    export DATABASE_URL="postgres://postgres:postgres@localhost/backpack-local"
fi
python manage.py db upgrade
