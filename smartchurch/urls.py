from django.urls import path
from .import people

app_name = 'church'
urlpatterns= [
        path('new-member',people.create_bio_data,name='new_member'),
        path('delete_bio/<str:pk>/',people.delete_bio,name='delete_bio'),
        path('update_member/<str:pk>/',people.Update_member,name='update_member'),

        path('peoples_children/<str:pk>/',people.peoples_children,name='peoples_children'),
        path('update_peoples_children/<str:pk>/',people.update_peoples_children,name='update_peoples_children'),
        path('delete_peoples_children/<str:pk>/',people.delete_peoples_children,name='delete_peoples_children'),

        path('baptism/<str:pk>/',people.baptisms,name='baptism'),
        path('update_baptism/<str:pk>/',people.update_baptism,name='update_baptism'),
        path('delete_baptism/<str:pk>/',people.delete_baptism,name='delete_baptism'),

        path('emmergency_contact/<str:pk>/',people.emmergency_contact,name='emmergency_contact'),
        path('update_emergency/<str:pk>/',people.update_emergency,name='update_emergency'),
        path('delete_emergency/<str:pk>/',people.delete_emergency,name='delete_emergency'),

        path('manage_members',people.manage_members,name='manage_members'),
        path('profile/<str:pk>/',people.profile,name='profile'),

        path('create_profile_peoples_children/<str:pk>/',people.create_profile_peoples_children,name='create_profile_peoples_children'),
        path('update_profile_peoples_children/<str:pk>/',people.update_profile_peoples_children,name='update_profile_peoples_children'),
        path('create_profile_baptisms/<str:pk>/',people.create_profile_baptisms,name='create_profile_baptisms'),
        path('update_profile_baptism/<str:pk>/',people.update_profile_baptism,name='update_profile_baptism'),
        path('create_profile_emmergency_contact/<str:pk>/',people.create_profile_emmergency_contact,name='create_profile_emmergency_contact'),
        path('update_profile_emergency/<str:pk>/',people.update_profile_emergency,name='update_profile_emergency'),
        path('update_profile_member/<str:pk>/',people.update_profile_member,name='update_profile_member'),

        path('new_member_status/<str:pk>/',people.new_member_status,name='new_member_status'),
        path('foundationclass_status/<str:pk>/',people.foundationclass_status,name='foundationclass_status'),
        path('member_status/<str:pk>/',people.member_status,name='member_status'),
        path('inactive_status/<str:pk>/',people.inactive_status,name='inactive_status'),
        path('deceased_status/<str:pk>/',people.deceased_status,name='deceased_status')


        
]