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
        return self.add_blog(title, subtitle, date, author, img_url, body, user_id)

    def delete(self, blog_id) -> bool:
        return self.delete_blog(blog_id)

    def get_all(self) -> list[dict] | None:
        return self.get_all_blogs()

    def get_by_id(self, blog_id: str) -> Blog | None:
        return self.get_blog_by_id(blog_id)

    def update(self, blog_id: str, title: str, subtitle: str, author: str, img_url: str, body: str) -> bool:
        return self.update_blog(blog_id, title, subtitle, author, img_url, body)

