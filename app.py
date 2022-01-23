from wsgiref.simple_server import make_server
from pyramid.config import Configurator

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('transaction', 'transactionservice/transaction/{transaction_id}')
        config.add_route('types', '/transactionservice/types/{type}')
        config.add_route('sum', '/transactionservice/sum/{transaction_id}')
        config.scan('core')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()