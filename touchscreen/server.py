import subprocess, threading

DJ_MODE = "GET /api/dj-mode HTTP/1.1"
PLAYLIST_MODE = "GET /api/playlist HTTP/1.1"

current_mode = 'autoplay'


def start_touchscreen_server(mode=''):
  global current_mode
  current_mode = mode
  proc = subprocess.Popen(
      ['python', '-u', 'touchscreen/flask_server.py'],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT
  )

  t = threading.Thread(target=output_reader, args=(proc,))
  t.start()


def output_reader(proc):
  global current_mode
  for line in iter(proc.stdout.readline, b''):
    decoded = line.decode('utf-8')
    if DJ_MODE in decoded:
      current_mode = 'autoplay'
      print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
      print("DJ MODE")
    if PLAYLIST_MODE in decoded:
      current_mode = 'playlist'
      print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
      print("PLAYLIST MODE")
    if not "GET /" in decoded:
      print(decoded)


def get_application_mode():
  global current_mode
  return current_mode
