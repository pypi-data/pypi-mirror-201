from sqlalchemy.sql.compiler import IdentifierPreparer

from diengine_connect.driver.query import quote_identifier


class ChIdentifierPreparer(IdentifierPreparer):

    quote_identifier = staticmethod(quote_identifier)

    def _requires_quotes(self, _value):
        return True
