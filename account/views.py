from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.contrib.auth import get_user_model  
from .forms import LoginForm,SignupForm, UserUpdateForm 
from django.contrib.auth.mixins import UserPassesTestMixin 
from django.shortcuts import redirect, resolve_url

User = get_user_model()  # カスタムユーザーモデルを取得する

'''トップページ'''
class TempView(generic.TemplateView):
    template_name = 'top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

class Logout(LogoutView):
    template_name ='logout_done.html'

'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object  # userとしてモデルインスタンスをコンテキストに追加
        return context

'''ユーザー登録情報の更新'''
class UserUpdate(OnlyYouMixin, generic.UpdateView):

    model = User
    form_class = UserUpdateForm
    template_name = 'account/user_form.html'

    def get_success_url(self):
        return resolve_url('account:my_page', pk=self.kwargs['pk'])

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Update"
        return context


'''サインアップ'''
class Signup(generic.CreateView):
    template_name = 'user_form.html'
    form_class =SignupForm

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect('account:signup_done')

    # データ送信
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Sign up"
        return context

'''サインアップ完了'''
class SignupDone(generic.TemplateView):
    template_name = 'sign_up_done.html'