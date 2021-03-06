# coding=utf-8
from . import types, exceptions, builders, validators
from kushki.v1 import handling


class Kushki(object):

    def __init__(self, merchant_id, language=types.Languages._default, currency=types.Currencies._default,
                 environment=types.Environments._default):
        self._merchant_id = merchant_id
        self._language = language
        self._currency = currency
        self._environment = environment

    currency = property(lambda self: self._currency)
    language = property(lambda self: self._language)
    merchant_id = property(lambda self: self._merchant_id)

    def _execute(self, klass, *args):
        """
        Ejecuta una peticion a la API.
        :param klass: Clase de RequestBuilder a usar.
        :param args: Argumentos adicionales.
        :return: El objeto Response obtenido.
        """

        instance = handling.RequestHandler(klass(self._environment, self.merchant_id, *args))
        return instance()

    def charge(self, token, amount):
        """
        Efectiviza un pago.
        :param token: Token a efectivizar.
        :param amount: Valor (objeto Amount) a comprobar respecto del token efectivo.
        :return: El objeto Response obtenido.
        """

        return self._execute(builders.ChargeRequestBuilder, token, amount)

    def deferred_charge(self, token, amount, months, interest):
        """
        Efectiviza un pago en cuotas.
        :param token: Token a efectivizar.
        :param amount: Valor (objeto Amount) a comprobar respecto del token efectivo.
        :param months: Cantidad de meses.
        :param interest: Interes aplicado.
        :return: El objeto Response obtenido.
        """

        validators.validate_months(months)
        return self._execute(builders.DeferredChargeRequestBuilder, token, amount, months, interest)

    def void_charge(self, ticket, amount):
        """
        Anula un pago.
        :param ticket: El ticket del pago a anular.
        :param amount: El monto (objeto Amount) del pago a anular.
        :return: El objeto Response obtenido.
        """

        return self._execute(builders.VoidRequestBuilder, ticket, amount)

    # NOT SUPPORTED ANYMORE
    #
    # def refund_charge(self, ticket, amount):
    #     """
    #     Devuelve un pago.
    #     :param ticket: El ticket del pago a devolver.
    #     :param amount: La cantidad a devolver.
    #     :return: El objeto Response obtenido.
    #     """
    #
    #     self._validate_amount(amount)
    #     return self._execute(builders.RefundRequestBuilder, ticket, amount)

    # THIS TRANSACTION GENERATES A TOKEN, AND IT IS NOT USEFUL BESIDE TESTING.
    # THIS ENTRY POINT IS ALREADY HIT BY THE JAVASCRIPT FRONT-END (the form) AND
    #   THUS DE BACKEND HAS NOTHING TO DO WITH IT.
    def request_token(self, card_params):
        """
        Obtiene un token para esos parametros.
        :param card_params: Un diccionario con los parametros de la tarjeta.
        :return: El objeto Response obtenido.
        """

        return self._execute(builders.TokenRequestBuilder, card_params)
