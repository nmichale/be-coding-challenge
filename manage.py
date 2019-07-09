import click
import bjoern

from family_tree.app import create_app

@click.command()
@click.option('-d', '--debug', is_flag=True)
@click.option('-p', '--port', type=click.INT, default=8000)
@click.option('-h', '--host', default='0.0.0.0')
def run_app(debug, port, host):
    app = create_app()
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app()
