import random
from typing import Dict, List


class SQLQueryGenerator:
    def __init__(self, schema: Dict[str, str], table_name: str,
                 enable_where: bool = True,
                 enable_order_by: bool = True,
                 enable_group_by: bool = True,
                 enable_having: bool = True,
                 enable_limit: bool = True):
        self.schema = schema
        self.table_name = table_name
        self.enable_where = enable_where
        self.enable_order_by = enable_order_by
        self.enable_group_by = enable_group_by
        self.enable_having = enable_having
        self.enable_limit = enable_limit

    def _select_columns(self, max_cols: int = 4) -> List[str]:
        column_names = list(self.schema.keys())
        num_cols = min(len(column_names), random.randint(1, max_cols))
        return random.sample(column_names, num_cols)

    def _build_where_clause(self) -> str:
        conditions = []
        for col, col_type in random.sample(list(self.schema.items()), k=min(2, len(self.schema))):
            if "INT" in col_type.upper() or "REAL" in col_type.upper():
                val = random.randint(1, 100)
                op = random.choice([">", "<", "=", ">=", "<="])
                conditions.append(f"{col} {op} {val}")
            elif "TEXT" in col_type.upper():
                val = random.choice(["'open'", "'remediated'", "'S1'", "'S2'"])
                op = random.choice(["=", "LIKE"])
                conditions.append(f"{col} {op} {val}")
            elif "DATE" in col_type.upper():
                val = "'2023-01-01'"
                op = random.choice(["<", ">", "="])
                conditions.append(f"{col} {op} {val}")

        if not conditions:
            return ""

        connector = random.choice(["AND", "OR"])
        return "WHERE " + f" {connector} ".join(conditions)

    def _build_group_by_clause(self, selected_cols: List[str]) -> str:
        groupable = [col for col in selected_cols if "TEXT" in self.schema[col].upper()]
        if not groupable:
            return ""
        return "GROUP BY " + ", ".join(random.sample(groupable, k=1))

    def _build_having_clause(self) -> str:
        numeric_cols = [col for col, t in self.schema.items() if "INT" in t.upper() or "REAL" in t.upper()]
        if not numeric_cols:
            return ""
        col = random.choice(numeric_cols)
        agg_func = random.choice(["AVG", "MAX", "SUM"])
        threshold = random.randint(10, 50)
        return f"HAVING {agg_func}({col}) > {threshold}"

    def _build_order_by_clause(self, selected_cols: List[str]) -> str:
        order_col = random.choice(selected_cols)
        direction = random.choice(["ASC", "DESC"])
        return f"ORDER BY {order_col} {direction}"

    def _build_limit_clause(self) -> str:
        return f"LIMIT {random.choice([5, 10, 20, 50])}"

    def generate_query(self) -> str:
        selected_cols = self._select_columns()
        select_clause = "SELECT " + ", ".join(selected_cols)
        from_clause = f"FROM {self.table_name}"

        query_parts = [select_clause, from_clause]

        if self.enable_where:
            where_clause = self._build_where_clause()
            if where_clause:
                query_parts.append(where_clause)

        if self.enable_group_by:
            group_by = self._build_group_by_clause(selected_cols)
            if group_by:
                query_parts.append(group_by)
                if self.enable_having:
                    having = self._build_having_clause()
                    if having:
                        query_parts.append(having)

        if self.enable_order_by:
            order_by = self._build_order_by_clause(selected_cols)
            query_parts.append(order_by)

        if self.enable_limit:
            query_parts.append(self._build_limit_clause())

        return " ".join(query_parts) + ";"
