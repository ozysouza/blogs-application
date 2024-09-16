from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug import Response
from datetime import datetime

from src.helpers.blogs_manager import BlogsManager
from src.helpers.mail_manager import MailManager
from src.helpers.log import Log
from src.helpers.forms import ContactForm, CreateBlogForm, LoginForm, CommentForm

# Setup logging
logger = Log().logger

# Setup Blogs Manager
blogs_manager = BlogsManager()

views = Blueprint('views', __name__)


# TODO: Refactor the code to use three-layer DatabaseManager, Restful Layer, BlogsManager

@views.route("/about")
def about_page() -> Response | str:
    """
    Renders the about page.

    Returns:
        str: The rendered HTML template for the about page.
    """
    # Ensure login_form is available for all routes.
    login_form = LoginForm()
    return render_template('about.html', login_form=login_form)


@views.route("/add-blog", methods=['GET', 'POST', 'PATCH'])
@login_required
def add_blog() -> Response | str:
    """
    Renders the page to create a new blog.

    Returns:
        str: The rendered HTML template for the create blog page.
    """
    # Ensure login_form is available for all routes.
    login_form = LoginForm()

    blog_form = CreateBlogForm()
    try:
        if blog_form.validate_on_submit():
            blogs_manager.add(blog_form.title.data,
                              blog_form.subtitle.data,
                              blog_form.img_url.data,
                              blog_form.content.data)
            return redirect(url_for('views.home_page'))
    except Exception as err:
        logger.error(f'Failed to add blog due: {err}')
    return render_template("add_blog.html", blog_form=blog_form, login_form=login_form)


@views.route("/add-comment/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def add_comment(blog_id) -> Response | str:
    """
    Add a comment into user's blog.

    Returns:
        str: Reloads the page and renders the new comment.
    """
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        try:
            comment = comment_form.comment.data
            blogs_manager.add_comment(blog_id, comment)
            flash('Comment successfully submitted.', 'success')
            return redirect(request.referrer)
        except Exception as err:
            logger.error(f'Failed to add comment: {err}')
            flash('Failed submitting comment. Please try again.')
            return redirect(request.referrer)
    return render_template("display_blog.html", comment_form=comment_form)


@views.route("/contact", methods=['GET', 'POST'])
def contact_page() -> Response | str:
    """
    Renders the contact page and handles form submissions.

    If the request method is POST, it processes the contact form and sends an email.

    Returns:
        str: The rendered HTML template for the contact page.
    """
    # Ensure login_form is available for all routes.
    login_form = LoginForm()

    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        try:
            mail_manager = MailManager()
            mail_manager.send_email(contact_form.username.data,
                                    contact_form.email.data,
                                    contact_form.number.data,
                                    contact_form.message.data)
            flash('Message successfully sent!', 'success')
            return redirect(url_for('views.contact_page'))
        except Exception as err:
            logger.error(f"Failed to send email: {err}")
            flash(f'Failed to send email, try again later!', 'danger')
            return render_template("contact.html", contact_form=contact_form)
    return render_template("contact.html", contact_form=contact_form, login_form=login_form)


@views.route("/delete-blog/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    if blogs_manager.delete(blog_id):
        flash('Blog deleted successfully!', 'success')
    else:
        flash('Failed to delete blog.', 'danger')
    return redirect(url_for('views.home_page'))


@views.route("/edit-blog", methods=['GET', 'POST'])
@login_required
def edit_blog() -> Response | str:
    # Ensure login_form is available for all routes.
    login_form = LoginForm()

    blog_id = request.args.get('blog_id') if request.method == 'GET' else None
    requested_blog = blogs_manager.get_by_id(blog_id)

    edit_form = CreateBlogForm()
    if request.method == 'POST':
        # Get blog_id from form data during POST
        blog_id = edit_form.blog_id.data
        requested_blog = blogs_manager.get_by_id(blog_id)

    try:
        if requested_blog:
            edit_form = CreateBlogForm(
                blog_id=blog_id,
                title=requested_blog.title,
                subtitle=requested_blog.subtitle,
                img_url=requested_blog.img_url,
                content=requested_blog.body)

            if edit_form.validate_on_submit():
                blogs_manager.update(
                    blog_id,
                    edit_form.title.data,
                    edit_form.subtitle.data,
                    edit_form.img_url.data,
                    edit_form.content.data)
                updated_blog = blogs_manager.get_by_id(blog_id)
                return render_template("display_blog.html", blog=updated_blog, login_form=login_form)
        else:
            logger.warning(f"Blog with id: {blog_id} not found.")
            return redirect(url_for('views.home_page'))
    except Exception as err:
        logger.error(f"Failed to fetch blog post: {err}")
        return redirect(url_for('views.home_page'))
    return render_template("add_blog.html", blog_form=edit_form, blog=requested_blog, is_edit=True,
                           login_form=login_form)


@views.route("/reading", methods=['GET', 'POST'])
def find_blog() -> Response | str:
    """
    Renders a specific blog post based on its index.

    Returns:
        str: The rendered HTML template for the blog post page.
    """
    # Ensure login_form is available for all routes.
    login_form = LoginForm()
    comment_form = CommentForm()

    blog_id = request.args.get('blog_id')
    try:
        requested_blog = blogs_manager.get_by_id(blog_id)
        requested_comments = blogs_manager.get_comments(int(blog_id))
        if not requested_blog:
            logger.warning(f"Blog with Id: {blog_id} not found.")
            return redirect(url_for('views.home_page'))
    except Exception as err:
        logger.error(f"Failed to fetch blog post: {err}")
        return redirect(url_for('views.home_page'))
    return render_template("display_blog.html", blog=requested_blog, login_form=login_form, comment_form=comment_form,
                           comments=requested_comments)


@views.route("/")
def home_page() -> Response | str:
    """
    Renders the home page with a list of blogs.

    Returns:
        str: The rendered HTML template for the home page.
    """
    # Ensure login_form is available for all routes.
    login_form = LoginForm()

    try:
        blogs = blogs_manager.get_all()
    except Exception as err:
        logger.error(f"Failed to fetch blogs: {err}")
        blogs = []
    return render_template("home.html",
                           all_blogs=blogs,
                           author="Oziel De Souza",
                           subtitle="Improving my coding skills!",
                           login_form=login_form)


@views.context_processor
def inject_year():
    return {'year': datetime.today().strftime('%Y')}
