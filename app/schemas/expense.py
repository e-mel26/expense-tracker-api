from marshmallow import Schema, fields


class ExpenseCreateSchema(Schema):
    amount = fields.Float(required=True)
    category_id = fields.Int(required=True)
    date = fields.Date(required=True)
    note = fields.Str(required=False, allow_none=True)


class ExpenseUpdateSchema(Schema):
    amount = fields.Float(required=False)
    category_id = fields.Int(required=False)
    date = fields.Date(required=False)
    note = fields.Str(required=False, allow_none=True)


class ExpenseOutSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float()
    category_id = fields.Int()
    user_id = fields.Int()
    date = fields.Date()
    note = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    from marshmallow import Schema, fields


class ExpenseSummaryQuerySchema(Schema):
    # optional date filters: YYYY-MM-DD
    start = fields.Date(required=False)
    end = fields.Date(required=False)


class ExpenseSummaryByCategorySchema(Schema):
    category_id = fields.Int(required=True)
    category_name = fields.Str(required=True)
    total = fields.Float(required=True)


class ExpenseSummaryOutSchema(Schema):
    start = fields.Date(allow_none=True)
    end = fields.Date(allow_none=True)
    total = fields.Float(required=True)
    by_category = fields.List(fields.Nested(ExpenseSummaryByCategorySchema), required=True)

    # app/schemas/expense.py
from marshmallow import Schema, fields, validate

# ... keep your existing schemas above ...

class ExpenseSummaryQuerySchema(Schema):
    # ISO date strings like "2026-02-01"
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class CategoryTotalSchema(Schema):
    category_id = fields.Int(required=True)
    category_name = fields.Str(required=True)
    total = fields.Float(required=True)


class DailyTotalSchema(Schema):
    date = fields.Date(required=True)
    total = fields.Float(required=True)


class ExpenseSummaryOutSchema(Schema):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    total_spent = fields.Float(required=True)
    by_category = fields.List(fields.Nested(CategoryTotalSchema), required=True)
    by_day = fields.List(fields.Nested(DailyTotalSchema), required=True)