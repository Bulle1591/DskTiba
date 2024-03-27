from django import forms
from .constants import MODEL_NAMES
from django.contrib.contenttypes.models import ContentType
from .models import AppGroup, Role, Permission


class UserGroupCreateForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=AppGroup.objects.all(), required=False, widget=forms.Select(
        attrs={'data-dropdown-parent': '#userGroupModal', 'data-placeholder': 'Select a Parent Group'}))

    class Meta:
        model = AppGroup
        fields = ['name', 'description', 'parent', 'status']  # Include all relevant fields

    def __init__(self, *args, **kwargs):
        super(UserGroupCreateForm, self).__init__(*args, **kwargs)

        STATUS_CHOICES = [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('locked', 'Locked'),
        ]
        self.fields['status'].widget = forms.Select(choices=STATUS_CHOICES,
                                                    attrs={'data-dropdown-parent': '#userGroupModal'})

    def clean_name(self):
        group_name = self.cleaned_data['name']
        # Exclude the current instance from the exists query
        if AppGroup.objects.exclude(pk=self.instance.pk).filter(name=group_name).exists():
            raise forms.ValidationError('Group with this name already exists.')
        return group_name


class ContentTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Use your dictionary to get the friendly name for the model
        return MODEL_NAMES.get(f'{obj.app_label} | {obj.model}', str(obj))


class PermissionForm(forms.ModelForm):
    content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.exclude(app_label__in=['auth', 'contenttypes', 'sessions', 'admin', 'guardian']),
        required=False,
        widget=forms.Select(
            attrs={'data-dropdown-parent': '#userPermissionModal', 'data-placeholder': 'Select a Module'})
    )

    class Meta:
        model = Permission
        fields = ['name', 'description', 'content_type']

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here
        return cleaned_data


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a role name'}),
            'permissions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.all()
