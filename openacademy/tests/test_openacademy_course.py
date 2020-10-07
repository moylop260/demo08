import psycopg2

from odoo.tests import TransactionCase
from odoo.tools import mute_logger


class OpenacademyCourseTest(TransactionCase):
    @mute_logger("odoo.sql_db")
    def test_course_name_and_description(self):
        with self.assertRaisesRegex(
            psycopg2.IntegrityError,
            'new row for relation "openacademy_course" violates check constraint'
            ' "openacademy_course_name_description_check"',
        ):
            self.env["openacademy.course"].create(
                {"name": "Testing course", "description": "Testing course"}
            )

    def test_course_duplicate(self):
        course = self.env["openacademy.course"].create(
            {"name": "Testing course", "description": "Description X"}
        )
        course2 = course.copy()
        course3 = course.copy()
        self.assertTrue(course2)
        self.assertEqual(course.name, "Testing course")
        self.assertEqual(course2.name, "Duplicate of Testing course")
        self.assertEqual(course3.name, "Duplicate of Testing course (1)")

    @mute_logger("odoo.sql_db")
    def test_name_duplicate(self):
        self.env["openacademy.course"].create(
            {"name": "Testing course", "description": "Description X"}
        )
        with self.assertRaisesRegex(
            psycopg2.IntegrityError,
            "duplicate key value violates unique "
            'constraint "openacademy_course_name_unique"',
        ):
            self.env["openacademy.course"].create({"name": "Testing course"})
