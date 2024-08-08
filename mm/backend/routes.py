from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, User, Income, Expense, Budget
from datetime import datetime

bp = Blueprint('routes', __name__)

# Route to create a user
@bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if email already exists
    existing_user_by_email = User.query.filter_by(email=email).first()

    if existing_user_by_email:
        return jsonify({'message': 'Email already exists'}), 409
    
    new_user = User(username=username, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating the user'}), 500
    
# Route to login
@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({
            'message': 'Login successful',
            'id': user.id
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Route to add income
@bp.route('/api/income', methods=['POST'])
def add_income():
    data = request.get_json()
    try:
        new_income = Income(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date'],
            user_id=data['user_id']
        )
        db.session.add(new_income)
        db.session.commit()
        return jsonify(new_income.as_dict()), 201
    except Exception as e:
        print(f"Error creating income: {e}")  
        db.session.rollback()
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

# Route to get all income for a user
@bp.route('/api/income/<int:user_id>', methods=['GET'])
def get_income(user_id):
    income_records = Income.query.filter_by(user_id=user_id).all()
    income_list = [record.as_dict() for record in income_records]
    return jsonify(income_list)

# Route to delete income by ID
@bp.route('/api/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    income = Income.query.get(id)
    if income:
        db.session.delete(income)
        db.session.commit()
        return jsonify({'message': 'Income deleted successfully'}), 200
    else:
        return jsonify({'message': 'Income not found'}), 404

# Route to update income by ID
@bp.route('/api/income/<int:income_id>', methods=['PUT'])
def update_income(income_id):
    data = request.get_json()
    try:
        income = Income.query.get(income_id)
        if not income:
            return jsonify({'message': 'Income not found'}), 404

        income.amount = data.get('amount', income.amount)
        income.category = data.get('category', income.category)
        income.description = data.get('description', income.description)
        income.date = data.get('date', income.date)
        income.user_id = data.get('user_id', income.user_id)

        db.session.commit()
        return jsonify(income.as_dict()), 200

    except Exception as e:
        print(f"Error updating income: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Route to add expense
@bp.route('/api/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    try:
        new_expense = Expense(  
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date'],
            user_id=data['user_id']
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify(new_expense.as_dict()), 201
    except Exception as e:
        print(f"Error creating expense: {e}")  
        db.session.rollback()
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

# Route to get all expenses for a user
@bp.route('/api/expense/<int:user_id>', methods=['GET'])
def get_expenses(user_id):  
    expense_records = Expense.query.filter_by(user_id=user_id).all() 
    expense_list = [record.as_dict() for record in expense_records] 
    return jsonify(expense_list)

# Route to delete expense by ID
@bp.route('/api/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):  
    expense = Expense.query.get(id)  
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200  
    else:
        return jsonify({'message': 'Expense not found'}), 404  

# Route to update expense by ID
@bp.route('/api/expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):  
    data = request.get_json()
    try:
        expense = Expense.query.get(expense_id)  
        if not expense:
            return jsonify({'message': 'Expense not found'}), 404  

        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        expense.description = data.get('description', expense.description)
        expense.date = data.get('date', expense.date)
        expense.user_id = data.get('user_id', expense.user_id)

        db.session.commit()
        return jsonify(expense.as_dict()), 200

    except Exception as e:
        print(f"Error updating expense: {e}")  
        return jsonify({'message': 'Internal server error'}), 500


# Route to get user by ID
@bp.route('/api/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Route to add budget
@bp.route('/api/budget', methods=['POST'])
def add_budget():
    data = request.get_json()
    try:
        new_budget = Budget(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            user_id=data['user_id']
        )
        db.session.add(new_budget)
        db.session.commit()
        return jsonify(new_budget.as_dict()), 201
    except Exception as e:
        print(f"Error creating budget: {e}")  
        db.session.rollback()
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500


# Route to get all budgets for a user
@bp.route('/api/budget/<int:user_id>', methods=['GET'])
def get_budgets(user_id):  
    budget_records = Budget.query.filter_by(user_id=user_id).all()  
    budget_list = [record.as_dict() for record in budget_records]  
    return jsonify(budget_list)

# Route to delete budget by ID
@bp.route('/api/budget/<int:id>', methods=['DELETE'])
def delete_budget(id):  
    budget = Budget.query.get(id)  
    if budget:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'}), 200  
    else:
        return jsonify({'message': 'Budget not found'}), 404  

# Route to update budget by ID
@bp.route('/api/budget/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):  
    data = request.get_json()
    try:
        budget = Budget.query.get(budget_id)  
        if not budget:
            return jsonify({'message': 'Budget not found'}), 404  

        budget.amount = data.get('amount', budget.amount)
        budget.category = data.get('category', budget.category)
        budget.description = data.get('description', budget.description)
        # Removed date update logic
        budget.user_id = data.get('user_id', budget.user_id)

        db.session.commit()
        return jsonify(budget.as_dict()), 200

    except Exception as e:
        print(f"Error updating budget: {e}")  
        return jsonify({'message': 'Internal server error'}), 500

