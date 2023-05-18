from django import forms


class CommentProductForm(forms.Form):
    """
    Форма для добавления нового комментария к товару
    """
    review = forms.CharField(max_length=2500, label='Комментарий', help_text='Оставьте ваш комментарий')
    name = forms.CharField(max_length=200, label='Имя', help_text='Имя')
    email = forms.EmailField(label='Email', help_text='Email')
