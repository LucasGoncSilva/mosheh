from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class Error403ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/403"""

        res: HttpResponse = self.client.get(reverse('err:403'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 403)
        self.assertEqual(
            res.context.get('message1'), 'Você não tem autorização para proseguir.'
        )
        self.assertEqual(
            res.context.get('message2'),
            'Retorne para onde estava ou vá para a homepage.',
        )


class Error404ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/404"""

        res: HttpResponse = self.client.get(reverse('err:404'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 404)
        self.assertEqual(
            res.context.get('message1'), 'O endereço requisitado não foi encontrado.'
        )
        self.assertEqual(
            res.context.get('message2'),
            'Retorne para onde estava ou vá para a homepage.',
        )


class Error500ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/500"""

        res: HttpResponse = self.client.get(reverse('err:500'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 500)
        self.assertEqual(
            res.context.get('message1'), 'Ocorreu um problema com o servidor.'
        )
        self.assertEqual(
            res.context.get('message2'), 'Informe o problema para a equipe do site.'
        )
