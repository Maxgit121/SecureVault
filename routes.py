from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Password, Category
from forms import RegistrationForm, LoginForm, PasswordForm, CategoryForm, SearchForm

# Home route
@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html', title='Password Manager')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Add default categories for new user
        default_categories = ['Personal', 'Work', 'Financial', 'Social Media']
        
        db.session.add(user)
        db.session.commit()
        
        # After commit to get user.id
        for cat_name in default_categories:
            category = Category(name=cat_name, user_id=user.id)
            db.session.add(category)
        
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing password entries"""
    passwords = Password.query.filter_by(user_id=current_user.id).order_by(Password.title).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    search_form = SearchForm()
    
    return render_template('dashboard.html', title='Dashboard', 
                           passwords=passwords, categories=categories, search_form=search_form)

# Add password route
@app.route('/password/add', methods=['GET', 'POST'])
@login_required
def add_password():
    """Add a new password entry"""
    form = PasswordForm()
    
    # Populate category choices
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category.choices = [(0, '-- No Category --')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        category_id = form.category.data if form.category.data != 0 else None
        
        password = Password(
            title=form.title.data,
            username=form.username.data,
            password=form.password.data,
            website=form.website.data,
            notes=form.notes.data,
            user_id=current_user.id,
            category_id=category_id
        )
        
        db.session.add(password)
        db.session.commit()
        
        flash('Password added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_password.html', title='Add Password', form=form)

# Edit password route
@app.route('/password/edit/<int:password_id>', methods=['GET', 'POST'])
@login_required
def edit_password(password_id):
    """Edit an existing password entry"""
    password = Password.query.get_or_404(password_id)
    
    # Check if the password belongs to the current user
    if password.user_id != current_user.id:
        abort(403)
    
    form = PasswordForm()
    
    # Populate category choices
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category.choices = [(0, '-- No Category --')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        password.title = form.title.data
        password.username = form.username.data
        password.password = form.password.data
        password.website = form.website.data
        password.notes = form.notes.data
        password.category_id = form.category.data if form.category.data != 0 else None
        
        db.session.commit()
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    elif request.method == 'GET':
        form.title.data = password.title
        form.username.data = password.username
        form.password.data = password.password
        form.website.data = password.website
        form.notes.data = password.notes
        form.category.data = password.category_id or 0
    
    return render_template('edit_password.html', title='Edit Password', form=form, password=password)

# View password route
@app.route('/password/view/<int:password_id>')
@login_required
def view_password(password_id):
    """View a single password entry with details"""
    password = Password.query.get_or_404(password_id)
    
    # Check if the password belongs to the current user
    if password.user_id != current_user.id:
        abort(403)
    
    return render_template('view_password.html', title=f'View Password - {password.title}', password=password)

# Delete password route
@app.route('/password/delete/<int:password_id>', methods=['POST'])
@login_required
def delete_password(password_id):
    """Delete a password entry"""
    password = Password.query.get_or_404(password_id)
    
    # Check if the password belongs to the current user
    if password.user_id != current_user.id:
        abort(403)
    
    db.session.delete(password)
    db.session.commit()
    
    flash('Password deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Add category route
@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add a new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id)
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_category.html', title='Add Category', form=form)

# Search passwords route
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """Search for passwords"""
    form = SearchForm()
    
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data if form.validate_on_submit() else request.args.get('query')
        
        # Search in title, username, website, and notes
        passwords = Password.query.filter(
            Password.user_id == current_user.id,
            (Password.title.contains(query) | 
             Password.username.contains(query) | 
             Password.website.contains(query) | 
             Password.notes.contains(query))
        ).all()
        
        return render_template('search_results.html', title='Search Results', 
                               passwords=passwords, query=query, form=form)
    
    return redirect(url_for('dashboard'))

# Filter by category route
@app.route('/category/<int:category_id>')
@login_required
def filter_by_category(category_id):
    """Filter passwords by category"""
    category = Category.query.get_or_404(category_id)
    
    # Check if the category belongs to the current user
    if category.user_id != current_user.id:
        abort(403)
    
    passwords = Password.query.filter_by(user_id=current_user.id, category_id=category_id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    search_form = SearchForm()
    
    return render_template('dashboard.html', title=f'Category: {category.name}', 
                           passwords=passwords, categories=categories, 
                           current_category=category, search_form=search_form)
