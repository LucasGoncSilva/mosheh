import queue
import threading

from account.models import User
from django.test import TestCase
from utils import xor


class XORTestCase(TestCase):
    def setUp(self) -> None:
        self.passphrase = User.objects.create_user(
            username='user',
            password='testing_passphrase',
            is_active=True,
        ).password

        self.q: queue.Queue = queue.Queue()
        self.num = 100_000

    def test_xor_return_values(self) -> None:
        """Tests raises and return values"""

        self.assertIsNone(xor(None, self.passphrase[21:]))  # type: ignore
        self.assertEqual(xor('', self.passphrase[21:]), '')  # type: ignore
        self.assertEqual(xor(5, self.passphrase[21:]), 5)  # type: ignore

    def test_xor_null_value(self) -> None:
        """Tests return values"""

        with open('secret/tests/sample.txt') as txt:
            lines: list[str] = txt.readlines()

            for line in lines:
                data: str = line.strip()

                encrypted_data: str = xor(data, self.passphrase[21:])

                decrypted_data: str = xor(
                    encrypted_data, self.passphrase[21:], encrypt=False
                )

                self.q.put(encrypted_data)
                self.q.put(decrypted_data)

        threading.Thread(target=self.process_xor, daemon=True).start()
        self.q.join()

    def process_xor(self) -> None:
        while True:
            data = self.q.get()

            self.assertNotIn('\x00', data)
            self.assertTrue(
                all(map(lambda x: x in range(0x110000), [ord(i) for i in data]))
            )

            self.q.task_done()
