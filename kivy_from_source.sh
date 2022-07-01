apt install python-pip python3-pip gir1.2-glib-2.0 libdbus-glib-1-2 libexpat1-dev libgirepository-1.0-1 \
   libpython3-dev libpython3.5-dev python-pip-whl python3-cffi-backend \
   python3-crypto python3-cryptography python3-dbus python3-dev python3-gi \
   python3-idna python3-keyring python3-keyrings.alt python3-pyasn1 \
   python3-secretstorage python3-setuptools python3-wheel python3-xdg \
   python3.5-dev evtest libmtdev-dev zlib1g-dev libfreetype6-dev liblcms1-dev \
   libopenjp2-7 libtiff5 libjpeg62-turbo-dev git git-man liberror-perl

pip install virtualenv

git clone https://github.com/kivy/kivy

virtualenv -p /usr/bin/python3 kivy_build

source kivy_build/bin/activate

pip install cython pillow

#cd kivy
#USE_SDL2=0 CFLAGS="-I/opt/vc/include/" make
USE_SDL2=0 CFLAGS="-I/opt/vc/include/" pip install ./kivy/
