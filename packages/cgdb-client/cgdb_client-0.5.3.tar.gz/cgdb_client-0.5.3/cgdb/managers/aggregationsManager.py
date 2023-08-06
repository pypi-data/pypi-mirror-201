from cgdb.resources.aggregation import Aggregation


class AggregationsManager:
    def aggregations(self):
        return [Aggregation("VAL"), Aggregation("AVG"), Aggregation("SUM"), Aggregation("MIN"), Aggregation("MAX"),
                Aggregation("TM"), Aggregation("TN"), Aggregation("TE"), Aggregation("MED")]
