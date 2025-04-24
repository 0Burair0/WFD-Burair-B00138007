from django.contrib import admin
from .models import User, Module, Enrollment, TrainerAssignment, ModuleFile

admin.site.register(User)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(TrainerAssignment)
admin.site.register(ModuleFile)