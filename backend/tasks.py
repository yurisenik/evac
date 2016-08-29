from __future__ import absolute_import

from celery import shared_task


def sync_to_database(data):
    from backend.models import Item, Evacuator, Mark, Organization, Parking
    from datetime import datetime

    for item in data['items']:

        evacuator = item['evacuator']
        try:
            evacuator_instance = Evacuator.objects.get(id_ext=evacuator['id'])
        except Evacuator.DoesNotExist:
            evacuator_instance = Evacuator(id_ext=evacuator['id'], number=evacuator['number'])
            evacuator_instance.save()

        mark = item['mark']
        try:
            mark_instance = Mark.objects.get(id_ext=mark['id'])
        except Mark.DoesNotExist:
            mark_instance = Mark(id_ext=mark['id'], title=mark['title'], sort=mark['sort'])
            mark_instance.save()

        organization = item['organization']
        try:
            organization_instance = Organization.objects.get(id_ext=organization['id'])
        except Organization.DoesNotExist:
            organization_instance = Organization(id_ext=organization['id'], title=organization['title'])
            organization_instance.save()

        parking = item['parking']
        try:
            parking_instance = Parking.objects.get(id_ext=parking['id'])
        except Parking.DoesNotExist:
            parking_instance = Parking(id_ext=parking['id'], title=parking['title'])
            parking_instance.save()

        try:
            item_instance = Item.objects.get(id_ext=item['id'])
            print('Already in db with pk={0}'.format(item_instance.pk))
        #            item_instance.date = datetime.strptime(item['date'],'%d.%m.%Y %H:%M')
        #            item_instance.save()
            item_instance.save()
        except Item.DoesNotExist:
            item_instance = Item(id_ext=item['id'], from_place=item['fromplace'], evacuator=evacuator_instance,
                                 mark=mark_instance, number=item['number'], organization=organization_instance,
                                 parking=parking_instance, active=item['active'], to_index=item['toindex'],
                                 sort=item['sort'], date=datetime.strptime(item['date'], '%d.%m.%Y %H:%M'))
            item_instance.save()
            print('Added item to db with pk={0}'.format(item_instance.pk))


@shared_task
def fetch_data():
    import requests

    url = 'http://krd.ru/ajax/evacuated_avto/list.json?parent=45&page='
    page = 1

    r = requests.get(url + str(page))
    data = r.json()
    print('Processing first page...')
    sync_to_database(data)
    pages_count = data['page_count']
    #    items_count = data['items_count']
    print('Total pages: {0}'.format(pages_count))

    for page in range(2, pages_count + 1):
        print('Processing page: {0}'.format(page))
        r = requests.get(url + str(page))
        data = r.json()
        sync_to_database(data)
