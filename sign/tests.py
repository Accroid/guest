from django.test import TestCase
from django.contrib.auth.models import User

class IndexPageTest(TestCase):
    "测试index登录首页"

    def test_index_page_renders_index_template(self):
        "测试index视图"
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateNotUsed(response,'index.html')

class LoginActionTest(TestCase):
    "测试登录动作"
    def setUp(self) -> None:
        User.objects.create_user('admin','admin@mail.com','admin123456')

    def test_add_admin(self):
        "测试添加用户"
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@mail.com')

    def test_login_action_username_password_null(self):
        "用户名密码为空"
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_success(self):
        "登录成功"
        test_data = {'username':'admin','password':'admin123456'}
        ersponse = self.client.post('/login_action/')