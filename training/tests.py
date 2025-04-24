from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Module, Enrollment, TrainerAssignment, ModuleFile

User = get_user_model()

class ProjectTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="password", role="admin")
        self.trainer = User.objects.create_user(username="trainer1", password="password", role="trainer")
        self.student = User.objects.create_user(username="student1", password="password", role="student")

        self.module = Module.objects.create(title="Intro Module", description="Start here")

    def test_create_module(self):
        count = Module.objects.count()
        self.assertEqual(count, 1)

    def test_edit_module(self):
        self.module.title = "Updated Title"
        self.module.save()
        self.assertEqual(Module.objects.get(id=self.module.id).title, "Updated Title")

    def test_delete_module(self):
        self.module.delete()
        self.assertEqual(Module.objects.count(), 0)

    def test_enroll_student(self):
        Enrollment.objects.create(user=self.student, module=self.module)
        self.assertEqual(Enrollment.objects.filter(user=self.student).count(), 1)

    def test_view_enrolled_modules(self):
        Enrollment.objects.create(user=self.student, module=self.module)
        enrolled = [e.module for e in Enrollment.objects.filter(user=self.student)]
        self.assertIn(self.module, enrolled)

    def test_assign_trainer(self):
        TrainerAssignment.objects.create(user=self.trainer, module=self.module)
        self.assertEqual(TrainerAssignment.objects.filter(user=self.trainer).count(), 1)

    def test_view_trainer_assignments(self):
        TrainerAssignment.objects.create(user=self.trainer, module=self.module)
        assigned = [a.module for a in TrainerAssignment.objects.filter(user=self.trainer)]
        self.assertIn(self.module, assigned)

    def test_add_module_file(self):
        ModuleFile.objects.create(module=self.module, week=1, title="W1 Notes", file="module_files/w1.pdf")
        self.assertEqual(ModuleFile.objects.count(), 1)
