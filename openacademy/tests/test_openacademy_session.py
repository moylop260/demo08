import psycopg2

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase
from odoo.tools import mute_logger


class OpenacademySessionTest(TransactionCase):
    def test_session_same_instructor_constraint(self):
        with self.assertRaisesRegex(
            ValidationError, "A session's instructor can't be an attendee"
        ):
            self.env["openacademy.session"].create(
                {
                    "name": "Testing course",
                    "course_id": self.env.ref("openacademy.course0").id,
                    "instructor_id": self.env.ref("base.res_partner_1").id,
                    "attendee_ids": [(4, self.env.ref("base.res_partner_1").id)],
                }
            )

    def test_session_happy_path(self):
        session = self.env["openacademy.session"].create(
            {
                "name": "Testing course",
                "course_id": self.env.ref("openacademy.course0").id,
                "instructor_id": self.env.ref("base.res_partner_1").id,
                "attendee_ids": [(4, self.env.ref("base.res_partner_2").id)],
                "seats": 1,
            }
        )
        self.assertTrue(session)
        self.assertEqual(session.name, "Testing course", "The session name is not good")

    def test_taken_seats(self):
        session = self.env["openacademy.session"].create(
            {
                "name": "Testing course",
                "course_id": self.env.ref("openacademy.course0").id,
                "instructor_id": self.env.ref("base.res_partner_1").id,
                "attendee_ids": [
                    (4, self.env.ref("base.res_partner_2").id),
                    (4, self.env.ref("base.res_partner_3").id),
                ],
                "seats": 2,
            }
        )
        session._taken_seats()
        self.assertEqual(session.taken_seats, 100)
        session.write({"seats": 4})
        session._taken_seats()
        self.assertEqual(session.taken_seats, 50)
        session.write({"seats": 0})
        session._taken_seats()
        self.assertEqual(session.taken_seats, 0)
        session.write({"seats": 1})
        session._taken_seats()
        self.assertEqual(session.taken_seats, 200)

    @mute_logger("odoo.sql_db")
    def test_session_without_required_course(self):
        with self.assertRaisesRegex(
            psycopg2.IntegrityError,
            'null value in column "course_id" violates not-null constraint',
        ):
            self.env["openacademy.session"].create(
                {
                    "name": "Testing course",
                    "instructor_id": self.env.ref("base.res_partner_1").id,
                    "attendee_ids": [(4, self.env.ref("base.res_partner_2").id)],
                }
            )
