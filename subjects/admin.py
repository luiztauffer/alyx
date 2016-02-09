from django.contrib import admin
from .models import *

class ResponsibleUserListFilter(admin.SimpleListFilter):
    title = 'responsible user'
    parameter_name = 'responsible_user'

    def lookups(self, request, model_admin):
        return (
            ('m', 'Me'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'm':
            return queryset.filter(responsible_user=request.user)

class SubjectAliveListFilter(admin.SimpleListFilter):
    title = 'alive'
    parameter_name = 'alive'

    def lookups(self, request, model_admin):
        return (
            ('y', 'Yes'),
            ('n', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'y':
            return queryset.filter(death_date_time=None)
        if self.value() == 'n':
            return queryset.exclude(death_date_time=None)


class WeighingsInline(admin.TabularInline):
    model = Weighing
    extra = 0
    ordering = ['start_date_time']
    fields = 'start_date_time', 'weight'
    readonly_fields = 'start_date_time', 'weight'

class NotesInline(admin.TabularInline):
    model = Note
    extra = 0
    ordering = ['start_date_time']
    fields = 'start_date_time', 'narrative'
    readonly_fields = 'start_date_time', 'narrative'

class SurgeriesInline(admin.TabularInline):
    model = Surgery
    extra = 0
    ordering = ['start_date_time']
    fields = 'procedure', 'start_date_time', 'brain_location'
    readonly_fields = 'procedure', 'start_date_time', 'brain_location'
    show_change_link = True

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'birth_date_time', 'responsible_user',
                    'strain', 'genotype', 'sex', 'alive']
    search_fields = ['nickname', 'responsible_user__first_name',
                     'responsible_user__last_name', 'responsible_user__username',
                     'strain', 'genotype']
    list_filter = [SubjectAliveListFilter, ResponsibleUserListFilter]
    inlines = [
        NotesInline,
        WeighingsInline,
        SurgeriesInline,
    ]

class SpeciesAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['binomial']
        return self.readonly_fields

    list_display = ['binomial', 'display_name']
    readonly_fields = []

class SurgeryAdmin(admin.ModelAdmin):
    list_display = ['procedure', 'subject', 'location', 'start_date_time']

class WeighingAdmin(admin.ModelAdmin):
    list_display = ['subject', 'weight']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['subject', 'narrative']

class LitterAdmin(admin.ModelAdmin):
    list_display = ['mother', 'father']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Litter, LitterAdmin)

admin.site.register(Species, SpeciesAdmin)
admin.site.register(Note, NoteAdmin)

admin.site.register(Weighing, WeighingAdmin)
admin.site.register(Surgery, SurgeryAdmin)