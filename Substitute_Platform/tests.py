from django.test import TestCase
from django.urls import reverse
from Substitute_Platform.models import Categories, Products, platform_user
from django.contrib.auth.models import User
from django.contrib import auth


class IndexPageTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('Substitute_Platform:index'))
        self.assertEqual(response.status_code, 200)


class DetailsPageTestCase(TestCase):

    def setUp(self):
        chips = Products.objects.create(
            name='Chips nature maxi format',
            stores='',
            nutrition_grade='c',
            url_openfoodfact=("https://fr.openfoodfacts.org/produit/"
                              "3168930010630/chips-nature-maxi-format-lay-s"),
            image_url=("https://static.openfoodfacts.org/images/products/"
                       "316/893/001/0630/front_fr.18.400.jpg"),
        )
        self.product = Products.objects.get(name='Chips nature maxi format')

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('Substitute_Platform:detail',
                                           args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('Substitute_Platform:detail',
                                           args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class SubstitutesListPageTestCase(TestCase):

    def setUp(self):
        cat1 = Categories.objects.create(name='cracker')
        cat2 = Categories.objects.create(name='fruits')
        cat3 = Categories.objects.create(name='vegetables')
        prod1 = Products.objects.create(
            name='Chips',
            stores='',
            nutrition_grade='c',
            url_openfoodfact='url',
            image_url='url',
        )
        prod2 = Products.objects.create(
            name='Curly',
            stores='',
            nutrition_grade='d',
            url_openfoodfact='url',
            image_url='url',
        )
        prod3 = Products.objects.create(
            name='Strawberry',
            stores='',
            nutrition_grade='a',
            url_openfoodfact='url',
            image_url='url',
        )
        prod4 = Products.objects.create(
            name='Apple',
            stores='',
            nutrition_grade='a',
            url_openfoodfact='url',
            image_url='url',
        )
        prod5 = Products.objects.create(
            name='Carots',
            stores='',
            nutrition_grade='a',
            url_openfoodfact='url',
            image_url='url',
        )
        prod6 = Products.objects.create(
            name='potatoe',
            stores='',
            nutrition_grade='c',
            url_openfoodfact='url',
            image_url='url',
        )
        prod1.categories.set([cat1, cat2, cat3])
        prod2.categories.set([cat1])
        prod3.categories.set([cat2])
        prod4.categories.set([cat2])
        prod5.categories.set([cat3])
        prod6.categories.set([cat3])

    def test_SubstitutesList_page_returns_200(self):
        response = self.client.get(reverse(
            'Substitute_Platform:substitutes_list', args=[5]))
        self.assertEqual(response.status_code, 200)

    def test_SubstitutesList_page_returns_404(self):
        response = self.client.get(reverse(
            'Substitute_Platform:substitutes_list', args=[312]))
        self.assertEqual(response.status_code, 404)


class AccountRegistrationAuthenticationPageTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com',
                                        'temporary')
        self.user = User.objects.get(username=user.username)

    def test_account_page_returns_200(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('Substitute_Platform:account'))
        self.assertEqual(response.status_code, 200)

    def test_account_page_returns_302(self):
        response = self.client.get(reverse('Substitute_Platform:account'))
        self.assertEqual(response.status_code, 302)

    def test_registration_page_returns_200(self):
        response = self.client.get(reverse('Substitute_Platform:registration'))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_returns_302(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('Substitute_Platform:registration'))
        self.assertEqual(response.status_code, 302)

    def test_authentication_page_returns_200(self):
        response = self.client.get(reverse(
            'Substitute_Platform:authentication'))
        self.assertEqual(response.status_code, 200)

    def test_authentication_page_returns_302(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse(
            'Substitute_Platform:authentication'))
        self.assertEqual(response.status_code, 302)

    def test_disconnection_connected_page_returns_302(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse(
            'Substitute_Platform:disconnection'))
        self.assertEqual(response.status_code, 302)

    def test_disconnection_disconnected_page_returns_302(self):
        response = self.client.get(reverse(
            'Substitute_Platform:disconnection'))
        self.assertEqual(response.status_code, 302)

    def test_account_change_mail(self):
        self.client.login(username='temporary', password='temporary')
        newMail = "newmail@gmail.com"
        response = self.client.post(reverse(
            'Substitute_Platform:account'), {
                'new_password1': "",
                'new_password2': "",
                'email': newMail
        })
        self.user.refresh_from_db()
        self.assertEqual(newMail, self.user.email)

    def test_account_change_password(self):
        self.client.login(username='temporary', password='temporary')
        newPassword = "Newpassword1"
        response = self.client.post(reverse(
            'Substitute_Platform:account'), {
                'new_password1': newPassword,
                'new_password2': newPassword,
                'email': ""
        })
        self.user.refresh_from_db()
        assert self.user.check_password(newPassword)
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_account_change_both(self):
        self.client.login(username='temporary', password='temporary')
        newMail = "newmail@gmail.com"
        newPassword = "Newpassword2"
        response = self.client.post(reverse(
            'Substitute_Platform:account'), {
                'new_password1': newPassword,
                'new_password2': newPassword,
                'email': newMail
        })
        self.user.refresh_from_db()
        self.assertEqual(newMail, self.user.email)
        assert self.user.check_password(newPassword)
        user = auth.get_user(self.client)
        assert user.is_authenticated


class LegalNoticePageTestCase(TestCase):

    def test_legal_notice_page_returns_200(self):
        response = self.client.get(reverse('Substitute_Platform:legal'))
        self.assertEqual(response.status_code, 200)


class MySubstitutesPageTestCase(TestCase):

    def setUp(self):

        user = User.objects.create_user('temporary', 'temporary@gmail.com',
                                        'temporary')

    def test_MySubstitutes_page_returns_200(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('Substitute_Platform:substitutes'))
        self.assertEqual(response.status_code, 200)

    def test_MySubstitutes_page_returns_302(self):
        response = self.client.get(reverse('Substitute_Platform:substitutes'))
        self.assertEqual(response.status_code, 302)


class SaveSubstitutePageTestCase(TestCase):

    def setUp(self):
        self.substituted_product = Products.objects.create(
            name='Chips',
            stores='',
            nutrition_grade='c',
            url_openfoodfact='url',
            image_url='url',
        )
        self.substituent_product = Products.objects.create(
            name='Carots',
            stores='',
            nutrition_grade='a',
            url_openfoodfact='url',
            image_url='url',
        )

        self.user = User.objects.create_user('temporary', 'temporary@gmail.com',
                                             'temporary')

    def test_new_substitute_is_saved(self):
        old_saved_substitutes = platform_user.objects.count()
        self.client.login(username='temporary', password='temporary')
        substituent_name = self.substituent_product.name
        substituted_name = self.substituted_product.name
        response = self.client.post(reverse(
            'Substitute_Platform:substitute_save'), {
                'checkbox': substituent_name,
                'substituted_name': substituted_name,
        })
        new_saved_substitutes = platform_user.objects.count()
        self.assertEqual(new_saved_substitutes, old_saved_substitutes + 1)


class RegisteringPageTestCase(TestCase):

    def setUp(self):
        self.password = 'temporary'
        self.username = 'temporary'
        self.email = 'temporary@gmail.com'

    def test_user_is_registered(self):
        old_user_count = User.objects.count()
        password = self.password
        username = self.username
        email = self.email
        response = self.client.post(reverse(
            'Substitute_Platform:registration'), {
                'password': password,
                'username': username,
                'email': email,
            })
        new_user_count = User.objects.count()
        user = auth.get_user(self.client)
        assert user.is_authenticated
        self.assertEqual(new_user_count, old_user_count + 1)


class connectionPageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary',
                                             'temporary@gmail.com', 'temporary')

    def test_user_is_connected(self):
        password = 'temporary'
        username = 'temporary'
        response = self.client.post(reverse(
            'Substitute_Platform:authentication'), {
                'username': username,
                'password': password,
            })
        user = auth.get_user(self.client)
        assert user.is_authenticated


class ProductSearchPageTestCase(TestCase):

    def setUp(self):
        prod1 = Products.objects.create(
            name='Nutella GR800 Gran Formato',
            stores='',
            nutrition_grade='e',
            url_openfoodfact='url',
            image_url='url',
        )
        prod2 = Products.objects.create(
            name='Nutella',
            stores='',
            nutrition_grade='e',
            url_openfoodfact='url',
            image_url='url',
        )
        prod3 = Products.objects.create(
            name='Nutella Barquette',
            stores='',
            nutrition_grade='e',
            url_openfoodfact='url',
            image_url='url',
        )

        def test_product_search_page_returns_200(self):
            response = self.client.get(reverse(
                'Substitute_Platform:substitutes_list') + '?query=nutella')
            self.assertEqual(response.status_code, 200)

        def test_product_search_page_returns_404(self):
            response = self.client.get(reverse(
                'Substitute_Platform:substitutes_list') + '?query=odbievd')
            self.assertEqual(response.status_code, 404)
