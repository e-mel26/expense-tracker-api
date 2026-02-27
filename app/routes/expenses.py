from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, extract
from flask import request

from app.extensions import db
from app.models import Expense, Category
from app.schemas import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseOutSchema,
    ExpenseSummaryQuerySchema,
    ExpenseSummaryOutSchema,
)

blp = Blueprint(
    "expenses",
    __name__,
    url_prefix="/expenses",
    description="Expenses CRUD",
)

# =============================
# CREATE + LIST EXPENSES
# =============================
@blp.route("/")
class ExpensesList(MethodView):
    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    @blp.arguments(ExpenseCreateSchema)
    @blp.response(201, ExpenseOutSchema)
    def post(self, data):
        """Create an expense"""
        user_id = int(get_jwt_identity())

        category = Category.query.get(data["category_id"])
        if not category:
            abort(404, message="Category not found.")

        expense = Expense(
            amount=data["amount"],
            category_id=data["category_id"],
            date=data["date"],
            note=data.get("note"),
            user_id=user_id,
        )

        try:
            db.session.add(expense)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error creating expense.")

        return expense

    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    @blp.response(200, ExpenseOutSchema(many=True))
    def get(self):
        """List expenses for current user"""
        user_id = int(get_jwt_identity())
        return (
            Expense.query.filter_by(user_id=user_id)
            .order_by(Expense.date.desc())
            .all()
        )


# =============================
# DATE RANGE SUMMARY
# =============================
@blp.route("/summary")
class ExpensesSummary(MethodView):
    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    @blp.arguments(ExpenseSummaryQuerySchema, location="query")
    @blp.response(200, ExpenseSummaryOutSchema)
    def get(self, args):
        user_id = int(get_jwt_identity())
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        if not start_date or not end_date:
            return {"message": "start_date and end_date are required"}, 400

        # total spent
        total_spent = (
            db.session.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
            .scalar()
        )

        # by category
        by_category_rows = (
            db.session.query(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .join(Expense, Expense.category_id == Category.id)
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
            .group_by(Category.id, Category.name)
            .order_by(func.sum(Expense.amount).desc())
            .all()
        )

        by_category = [
            {
                "category_id": r.category_id,
                "category_name": r.category_name,
                "total": float(r.total),
            }
            for r in by_category_rows
        ]

        # by day
        by_day_rows = (
            db.session.query(
                Expense.date.label("date"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
            .group_by(Expense.date)
            .order_by(Expense.date.asc())
            .all()
        )

        by_day = [{"date": r.date, "total": float(r.total)} for r in by_day_rows]

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_spent": float(total_spent),
            "by_category": by_category,
            "by_day": by_day,
        }


# =============================
# MONTHLY SUMMARY (NEW)
# =============================
@blp.route("/summary/monthly")
class ExpensesMonthlySummary(MethodView):
    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    def get(self):
        year = request.args.get("year", type=int)
        if not year:
            return {"message": "year query param is required"}, 400

        user_id = int(get_jwt_identity())

        rows = (
            db.session.query(
                extract("month", Expense.date).label("month"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .filter(
                Expense.user_id == user_id,
                extract("year", Expense.date) == year,
            )
            .group_by("month")
            .order_by("month")
            .all()
        )

        return [
            {"month": f"{year}-{int(r.month):02d}", "total": float(r.total)}
            for r in rows
        ]


# =============================
# EXPENSE DETAIL (GET/PUT/DELETE)
# =============================
@blp.route("/<int:expense_id>")
class ExpenseDetail(MethodView):
    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    @blp.response(200, ExpenseOutSchema)
    def get(self, expense_id):
        user_id = int(get_jwt_identity())
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

        if not expense:
            abort(404, message="Expense not found.")

        return expense

    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    @blp.arguments(ExpenseUpdateSchema)
    @blp.response(200, ExpenseOutSchema)
    def put(self, data, expense_id):
        user_id = int(get_jwt_identity())
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

        if not expense:
            abort(404, message="Expense not found.")

        if "category_id" in data:
            category = Category.query.get(data["category_id"])
            if not category:
                abort(404, message="Category not found.")

        for key, value in data.items():
            if value is not None:
                setattr(expense, key, value)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error updating expense.")

        return expense

    @jwt_required()
    @blp.doc(security=[{"BearerAuth": []}])
    def delete(self, expense_id):
        user_id = int(get_jwt_identity())
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

        if not expense:
            abort(404, message="Expense not found.")

        try:
            db.session.delete(expense)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error deleting expense.")

        return {"message": "Expense deleted successfully"}