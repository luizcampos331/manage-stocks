import os

from app.infra.gateways.stock_values_gateway import PolygonStockValuesGateway

implementations = {
    "polygon": PolygonStockValuesGateway,
}


class StockValuesGatewayFactory:
    @staticmethod
    def make():
        implementation = os.getenv("STOCK_VALUES_IMPLEMENTATION")
        if implementation not in implementations:
            raise ValueError(
                f"Unsupported STOCK_VALUES_IMPLEMENTATION: {implementation}"
            )

        return implementations[implementation]()
