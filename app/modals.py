from .forms import UserAddForm, UserUpdateForm, CustomerAddForm, CustomerUpdateForm, PersonnelAddForm, PersonnelUpdateForm

# # # Dictionaries # # #
user_add_modal = {'id': 'User-Add-Modal',
                    'aria_label': 'User-Add-Modal',
                    'title_id': 'User-Add-Modal',
                    'title': 'Add User',
                    'form_id': UserAddForm.form_id}

user_update_modal = {'id': 'User-Update-Modal',
                     'aria_label': 'User-Update-Modal',
                     'title_id': 'User-Update-Modal',
                     'title': 'Update User',
                     'form_id': UserUpdateForm.form_id}

customer_add_modal = {'id': 'Customer-Add-Modal',
                      'aria_label': 'Customer-Add-Modal',
                      'title_id': 'Customer-Add-Modal',
                      'title': 'Add Customer',
                      'form_id': CustomerAddForm.form_id}



customer_update_modal = {'id': 'Customer-Update-Modal',
                         'aria_label': 'Customer-Update-Modal',
                         'title_id': 'Customer-Update-Modal',
                         'title': 'Update Customer',
                         'form_id': CustomerUpdateForm.form_id}

personnel_add_modal = {'id': 'Personnel-Add-Modal',
                         'aria_label': 'Personnel-Add-Modal',
                         'title_id': 'Personnel-Add-Modal',
                         'title': 'Add Personnel',
                         'form_id': PersonnelAddForm.form_id}

personnel_update_modal = {'id': 'Personnel-Update-Modal',
                         'aria_label': 'Personnel-Update-Modal',
                         'title_id': 'Personnel-Update-Modal',
                         'title': 'Update Personnel',
                         'form_id': PersonnelUpdateForm.form_id}

### Classes ###
# - Work in progress. -Joe Flack, 03/31/2016
class UserAddModal:
    id = 'User-Add-Modal'
    aria_label = 'User-Add-Modal'
    title_id = 'User-Add-Modal'
    title = 'Add New User'


class UserUpdateModal:
    id = 'User-Update-Modal'
    aria_label = 'User-Update-Modal'
    title_id = 'User-Update-Modal'
    title = 'Update User'

def __init__(self, id, aria_label, title_id, title):
    self.id = id
    self.aria_label = aria_label
    self.title_id = title_id
    self.title = title


def __repr__(self):
    return '<id {}>'.format(self.id)
