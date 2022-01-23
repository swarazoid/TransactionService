import json

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from core.controller import Transaction, TransactionCoordinator


@view_defaults(route_name='/transactionservice')
class TransactionServiceViews:
    def __init__(self, request):
        self.transaction_coordinator = TransactionCoordinator()
        self.request = request

    @view_config(route_name='transaction', request_method=["GET", "PUT"])
    def transaction_details(self):
        try:
            transaction_id = int(self.request.matchdict["transaction_id"])
            if self.request.method == "GET":
                response, status = self.transaction_coordinator.get_transaction(transaction_id)
                return Response(body=json.dumps(response), status=status)
            elif self.request.method == "PUT":
                body = self.request.json_body
                body["transaction_id"] = transaction_id
                transaction = Transaction(body)
                response, status = self.transaction_coordinator.update_transaction(transaction)
                return Response(body=json.dumps(response), status=status)
        except Exception as e:
            return Response(body=json.dumps({"message": str(e)}), status=500)

    @view_config(route_name='types', request_method=["GET"])
    def get_transactions_for_a_type(self):
        try:
            type = self.request.matchdict["type"]
            response, status = self.transaction_coordinator.get_transactions_of_a_type(type)
            return Response(body=json.dumps(response), status=status)
        except Exception as e:
            return Response(body=json.dumps({"message": str(e)}), status=500)

    @view_config(route_name='sum', request_method=["GET"])
    def get_transaction_sum(self):
        try:
            transaction_id = int(self.request.matchdict["transaction_id"])
            response, status = self.transaction_coordinator.get_sum_of_related_transactions(transaction_id)
            return Response(body=json.dumps(response), status=status)
        except Exception as e:
            return Response(body=json.dumps({"message": str(e)}), status=500)

