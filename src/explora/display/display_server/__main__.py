from . import main, HOST, PORT, STATIC_DIR
import argparse


parser = argparse.ArgumentParser(
                    prog='Explora HAT | Display server',
                    description="""An HTTP/Websocket server to display interactive content on a browser. 
Mainly designed to be used in Kiosk mode""")

parser.add_argument('--host', default=HOST, 
                    help='Bind the socket to this host. Use 0.0.0.0 to allow all remote connections')
parser.add_argument('-p', '--port', default=PORT, 
                    help='Bind socket to this port. If 0, an available port will be picked')
parser.add_argument('-d', '--static-dir', default=STATIC_DIR, 
                    help="The local directory from where to serve static files")
parser.add_argument('--static-path', default="/", 
                    help="The path where to make the static files available")

args = parser.parse_args()

main(args.host, args.port, (args.static_path, args.static_dir))