[
  {
    "question": "What is the total number of orders?",
    "expected_tables": ["orders"],
    "expected_metric": "count"
  },
  {
    "question": "Find the top 10 product categories by revenue",
    "expected_tables": ["order_items", "products"],
    "expected_metric": "sum"
  },
  {
    "question": "Calculate monthly order growth",
    "expected_tables": ["orders"],
    "expected_metric": "monthly_count"
  }
]