from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from authority.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'phone_number',
            'tools',
        )

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on authority.User.
    list_display = ('username', 'last_name', 'first_name',)
    list_filter = ('last_name',)
    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'last_name', 'first_name', 'patronymic', 'email', 'phone_number', 'groups',
            'role', 'tools',)}),
        ('Права доступа', {'fields': ('is_active', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password', 'confirm_password', 'last_name', 'first_name', 'patronymic',
                'email', 'phone_number', 'role', 'tools',)}),
        ('Права доступа', {'fields': ('is_active', 'user_permissions')}),
    )
    search_fields = ('username', 'email', 'last_name')
    ordering = ('id', 'username')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
