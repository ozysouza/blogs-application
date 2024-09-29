from dataclasses import dataclass
from datetime import datetime
from src.helpers.models import Blog
from src.database.mysql_manager import MysqlManager

from flask_login import current_user


@dataclass()
class BlogsManager(MysqlManager):

    def add(self, title: str, subtitle: str, img_url: str, body: str) -> bool:
        date = datetime.today().strftime("%d/%m/%Y")
        author = f"{current_user.first_name} {current_user.last_name}"
        user_id = current_user.get_id()
        return self.sql_add_blog(title, subtitle, date, author, img_url, body, user_id)

    def add_comment(self, blog_id: int, comment: str) -> bool:
        return self.sql_add_comment(current_user.get_id(), blog_id, comment)

    def delete(self, blog_id: str) -> bool:
        return self.sql_delete_blog(blog_id)

    def delete_comment(self, comment_id: int) -> bool:
        return self.sql_delete_comment_by_id(comment_id)

    def get_all(self) -> list[dict] | None:
        return self.sql_get_all_blogs()

    def get_by_id(self, blog_id: str) -> Blog | None:
        return self.sql_get_blog_by_id(blog_id)

    def get_comments_by_blog(self, blog_id: int) -> list[dict] | None:
        return self.sql_get_comments_by_blog(blog_id)

    def get_comment_by_id(self, comment_id: int) -> dict | None:
        return self.sql_get_comment_by_id(comment_id)

    def update(self, blog_id: str, title: str, subtitle: str, img_url: str, body: str) -> bool:
        return self.sql_update_blog(blog_id, title, subtitle, img_url, body)

    def update_comment(self, comment_id: int, text: str) -> bool:
        return self.sql_update_comment(comment_id, text)
