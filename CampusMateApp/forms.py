from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import CommunityThread, CommunityReply, CATEGORY_CHOICES, Profile, DEPARTMENT_CHOICES, YEAR_CHOICES

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'w-full p-3 border border-[#C4C4C5] rounded-md bg-[#F2F2F2] text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#7A859D]'
        }
        for field_name in ['username', 'email', 'first_name', 'last_name']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(common_attrs)

        # Explicitly apply to password fields with PasswordInput widget
        if 'password1' in self.fields:
            self.fields['password1'].widget = PasswordInput(attrs=common_attrs)
        if 'password2' in self.fields:
            self.fields['password2'].widget = PasswordInput(attrs=common_attrs)

        self.fields['email'].required = True # Make email required if not already


class CommunityThreadForm(forms.ModelForm):
    class Meta:
        model = CommunityThread
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300',
                'placeholder': 'Enter thread title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300',
                'rows': 8,
                'placeholder': 'Describe your question or topic in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = CATEGORY_CHOICES


class CommunityReplyForm(forms.ModelForm):
    class Meta:
        model = CommunityReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300',
                'rows': 4,
                'placeholder': 'Write your reply...'
            })
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_id', 'department', 'year', 'profile_picture']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300',
                'placeholder': 'Enter your student ID...'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300'
            }),
            'year': forms.Select(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full p-3 border border-[#C4C4C4] dark:border-[#404040] rounded-md bg-[#F2F2F2] dark:bg-[#1a1a1a] text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7A859D] dark:focus:ring-[#404F68] transition-colors duration-300',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].choices = [('', 'Select Department')] + list(DEPARTMENT_CHOICES)
        self.fields['year'].choices = [('', 'Select Year')] + list(YEAR_CHOICES)
