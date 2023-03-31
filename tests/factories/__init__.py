import random
from datetime import date

import factory
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory
from faker import Faker

from authority.models import User, UserRoles
from control_panel.models import PanelTool, TaskResult
from eva.isiao.models import GIS, Indicator
from eva.models import EvaTool
from eva.reports.models import Category, Reports
from portal.models import Tools

faker = Faker()


class ToolsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tools

    full_name = factory.Faker('name')
    logo_pic = factory.django.ImageField()
    main_url = factory.Faker('url')

    @factory.post_generation
    def my_polymorphic_ctype(self, create, extracted, **kwargs):
        if not create:
            return

        self.my_polymorphic_ctype = ContentType.objects.get_for_model(self)

    @factory.post_generation
    def my_polymorphic_object(self, create, extracted, **kwargs):
        if not create:
            return

        self.my_polymorphic_object = self.my_polymorphic_ctype.get_object_for_this_type(id=self.id)


class PanelToolFactory(ToolsFactory):

    class Meta:
        model = PanelTool

    full_name = factory.Sequence(lambda n: f"PanelTool{n}")
    main_url = factory.Sequence(lambda n: f"http://paneltool{n}.com")


class EvaToolFactory(ToolsFactory):

    class Meta:
        model = EvaTool

    full_name = factory.Sequence(lambda n: f"EvaTool{n}")
    main_url = factory.Sequence(lambda n: f"http://evatool{n}.com")


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.user_name())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    password = factory.LazyAttribute(lambda x: make_password('12345678qwerty'))
    is_active = True

    @factory.post_generation
    def tools(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tool in extracted:
                self.tools.add(tool)


class SimpleUserFactory(UserFactory):

    role = UserRoles.USER


class AdminFactory(UserFactory):

    role = UserRoles.ADMIN


class AdminEvaFactory(UserFactory):

    role = UserRoles.ADMIN_EVA


class TaskResultFactory(DjangoModelFactory):

    class Meta:
        model = TaskResult

    date = factory.lazy_attribute(lambda x: date.today())
    periodicity = factory.lazy_attribute(lambda obj: random.choice(TaskResult.Periodic.choices)[0])
    color = factory.lazy_attribute(lambda obj: random.choice(TaskResult.Colors.choices)[0])
    full_name = factory.Faker('name')
    body = factory.Faker('text')


class GISFactory(DjangoModelFactory):

    class Meta:
        model = GIS

    full_name = factory.lazy_attribute(lambda obj: 'Full name of ' + obj.short_name)
    short_name = factory.Sequence(lambda n: 'gis{}'.format(n))
    dashboard_code = factory.Sequence(lambda n: f"system_{n}")
    zammad_systemcode = factory.Sequence(lambda n: n * 10)


class IndicatorFactory(DjangoModelFactory):

    class Meta:
        model = Indicator

    full_name = factory.Faker('text', max_nb_chars=250)
    ias_code = factory.Faker('ean13')
    periodicity = 'day'
    zammad_queryset = factory.Faker('sentence')


class CategoryFactory(DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    serial_number = factory.Sequence(lambda n: n)


class ReportsFactory(DjangoModelFactory):

    class Meta:
        model = Reports

    name = factory.Sequence(lambda n: f'Reports {n}')
    serial_number = factory.Sequence(lambda n: n)
    zammad_queryset = factory.Faker('text')
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)
