from django.contrib import admin

from django.http import FileResponse, HttpResponseRedirect
from xlsxwriter.workbook import Workbook

from .models import People, Otdel, Profile


admin.site.register(Otdel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'otdel']

admin.site.register(Profile, ProfileAdmin)


@admin.register(People)
class people(admin.ModelAdmin):
    list_display = ['name', 'nIb', 'room', 'date', 'otdel']
    list_filter = ['otdel']
    actions = ['getExcel']
    
    
    def getExcel(modelAdmin, request, queryset):
        data = ['ФИО', '№ ИБ', 'Дата госпитализации', '№ палаты']

        workbook = Workbook('output.xlsx')
        worksheet = workbook.add_worksheet()
        for i, el in enumerate(data):
            worksheet.write(0, i, el)

        for i, el in enumerate(queryset):
            worksheet.write(i+1, 0, el.name)
            worksheet.write(i+1, 1, el.nIb)
            worksheet.write(i+1, 2, el.date)
            worksheet.write(i+1, 3, el.room)
        workbook.close()
        return FileResponse(open('output.xlsx', 'rb'))

    getExcel.short_description = "Выгрузка в excel"


    # def getPin(self, request, queryset):
    #     if 'apply' in request.POST:
    #         queryset.update(status='NEW_STATUS')
    #         self.message_user(request,
    #                           "Changed status on {} orders".format(queryset.count()))
    #         return HttpResponseRedirect(request.get_full_path())

    #     return render(request,
    #                   'order_intermediate.html',
    #                   context={})

    # getPin.short_description = 'ПИН лист'
