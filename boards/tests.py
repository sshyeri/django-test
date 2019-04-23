from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from .models import Board
from .forms import BoardForm

class SettingsTest(TestCase):
    def test_01_settings(self):
        #assertEqual: 같지 않으면 경고한다. 쟝고 테스트 플러스의 메서드
        self.assertEqual(settings.USE_I18N, True)
        self.assertEqual(settings.USE_TZ, False)
        self.assertEqual(settings.LANGUAGE_CODE, 'ko-kr')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Seoul')
        
#2. Model test + ModelForm Test
class BoardModelTest(TestCase):
    def test_01_model(self):
        # board = Board.objects.create(title='test title', content='test content')
        board = Board.objects.create(title='test title', content='test content', user_id=1)
        self.assertEqual(str(board), f'Board{board.pk}', msg='출력 값이 일치하지 않음')
        # self.assertEqual(str(board), f'Board{board.title}', msg='출력 값이 일치하지 않음')
    def test_02_boardform(self):
        # given
        data = {'title': '제목', 'content': '내용'}
        # when then
        self.assertEqual(BoardForm(data).is_valid(), True)
        
    def test_03_boardform_without_title(self):
        data = {'content': '내용'}
        self. assertEqual(BoardForm(data).is_valid(), False)
 
    def test_04_boardform_without_content(self):
        data = {'title': '제목'}
        self. assertEqual(BoardForm(data).is_valid(), False)
        
#3. View test
class BoardViewTest(TestCase):
    # create test 에서의 포인트는 form을 제대로 주느냐이다.
    # 가장 기본은 get_check_200
    def SetUp(self):
        # given
        user = self.make_user(username='test', password='qawsedrf!')
        # when
        with self.login(username='test', password='qawsedrf!'):
            response = self.get_check_200('boards:create')
            # then
            # self.assertContains(response, '<form')
            self.assertIsInstance(response.context['form'], BoardForm)
    def test_02_get_create_login_required(self):
        self.assertLoginRequired('boards:create')
        
    def test_03_post_create(self):
        # given 사용자와 작성한 글 데이터
        user = self.make_user(username='test', password='qawsedrf!')
        data = { 'title': 'test title', 'content' : 'test content' }
        # when 로그인을 해서 post 요청으로 해당 url로 요청 보낸 경우
        with self.login(username='test', password='qawsedrf!'):
            # then 글이 작성되고, 페이지가 detail로 redirect 된다.
            self.post('boards:create', data=data)
            
    def test_04_board_create_witthout_content(self):
        # given
        user = self.make_user(username='test', password='qawsedrf!')
        data = {'title': 'test title' }
        # when
        with self.login(username='test', password='qawsedrf!'):
            response = self.post('boards:create', data=data)
            self.assertContains(response, '')
            # self.assertContains(response, '폼에 필수 항목입니다.')
            # form.is_valid()를 통과하지 못해서 팅겨저 나옴.
            # assertContains response 해당하는 글자가 있는지 확인하는 메소드