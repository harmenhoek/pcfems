# blog/dynamic_preferences_registry.py

from dynamic_preferences.types import BooleanPreference, StringPreference, ChoicePreference, IntegerPreference, LongStringPreference, DurationPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

# we create some section objects to link related preferences together

general = Section('general')
discussion = Section('manage')
item = Section('item')
user = Section('user')
message = Section('message')
nomenclature = Section('nomenclature')
check = Section('check')

# All preference types: https://github.com/agateblue/django-dynamic-preferences/blob/develop/dynamic_preferences/types.py

# ------------------------------------ GENERAL ------------------------------------

@global_preferences_registry.register
class ShowVersion(BooleanPreference):
    section = general
    name = 'show_version'
    verbose_name = "Show version number in footer"
    default = True
    required = True

@global_preferences_registry.register
class DefaultSortCol(ChoicePreference):
    section = general
    choices = [
        ('0', 'ID'),
        ('1', 'Image'),
        ('2', 'Item'),
        ('3', 'Category'),
        ('4', 'Location'),
        ('5', 'Status'),
        ('6', 'User'),
        ('7', 'Flag'),
        ('8', 'Description'),
        ('9', 'Serial'),
        ('10', 'Storage Location'),
        ('11', 'QR id'),
        ('12', 'Date in use'),
    ]
    name = 'default_sort_col'
    verbose_name = "Default sort column on the Items (home) page"
    default = '2'
    required = True

@global_preferences_registry.register
class DefaultSortColDirection(ChoicePreference):
    section = general
    choices = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]
    name = 'default_sort_col_direction'
    verbose_name = "Default sort column directions on the Items (home) page"
    default = "asc"
    required = True

@global_preferences_registry.register
class ImageItemMaxSize(ChoicePreference):
    section = general
    name = 'image_item_maxsize'
    choices = [
        ('600', '600'),
        ('800', '800'),
        ('1000', '1000'),
        ('1200', '1200'),
        ('1600', '1600'),
        ('2000', '2000'),
        ('10000', '10000'),
    ]
    verbose_name = "Maximum dimension of a newly uploaded item image. Existing images are not resized."
    default = '1000'
    required = True

@global_preferences_registry.register
class ImageCabinetLabSetupMaxSize(ChoicePreference):
    section = general
    name = 'image_cabinetlabsetup_maxsize'
    choices = [
        ('600', '600'),
        ('800', '800'),
        ('1000', '1000'),
        ('1200', '1200'),
        ('1600', '1600'),
        ('2000', '2000'),
        ('10000', '10000'),
    ]
    verbose_name = "Maximum dimension of a newly uploaded cabinet/lab/setup image. Existing images are not resized."
    default = '1000'
    required = True

# ------------------------------------ ITEM ------------------------------------

@global_preferences_registry.register
class ShowLogbook(BooleanPreference):
    section = item
    name = 'show_logbook'
    verbose_name = "Show the logbook on the image detail page"
    default = True
    required = True

@global_preferences_registry.register
class ShowHistory(BooleanPreference):
    section = item
    name = 'show_history'
    verbose_name = "Show item history on the image detail page"
    default = True
    required = True

# ------------------------------------ MESSAGE ------------------------------------

@global_preferences_registry.register
class LoginScreenMessageOn(BooleanPreference):
    section = message
    name = 'loginscreen_message_on'
    verbose_name = "Show a message on the login screen"
    default = False
    required = False

@global_preferences_registry.register
class LoginScreenMessage(LongStringPreference):
    section = message
    name = 'loginscreen_message'
    verbose_name = "Message on the login screen"
    default = ""
    required = False

@global_preferences_registry.register
class LoginScreenMessageType(ChoicePreference):
    section = message
    name = 'loginscreen_message_type'
    choices = [
        ('success', 'Green'),
        ('danger', 'Red'),
        ('warning', 'Yellow'),
        ('info', 'Light blue'),
        ('secondary', 'Grey'),
        ('primary', 'Blue'),
    ]
    verbose_name = "Color of the message box."
    default = "info"
    required = True

# @global_preferences_registry.register
# class AfterUpdateMessageOn(BooleanPreference):
#     section = message
#     name = 'afterupdate_message_on'
#     verbose_name = "Show a one-time message after an update has been pushed."
#     default = False
#     required = False
#
# @global_preferences_registry.register
# class AfterUpdateMessage(LongStringPreference):
#     section = message
#     name = 'afterupdate_message'
#     verbose_name = "Message of the one-time message after an update."
#     default = ""
#     required = False


# ------------------------------------ NOMENCLATURE ------------------------------------


@global_preferences_registry.register
class SiteTitle(StringPreference):
    section = nomenclature
    name = 'title'
    verbose_name = "EMS name in the main top navigation bar"
    default = 'PCF'
    required = True

@global_preferences_registry.register
class PageTitle(StringPreference):
    section = nomenclature
    name = 'pagetitle'
    verbose_name = "EMS name in browser"
    default = 'PCF EMS'
    required = True

@global_preferences_registry.register
class Footer(StringPreference):
    section = nomenclature
    name = 'footer'
    verbose_name = "Text to show in footer"
    default = "Equipment Management System for the Physics of Complex Fluids Group at the University of Twente."
    required = True

@global_preferences_registry.register
class RoomName(StringPreference):
    section = nomenclature
    name = 'room_name'
    verbose_name = "Name of room throughout the system."
    default = "Lab"
    required = True

@global_preferences_registry.register
class RoomNamePlural(StringPreference):
    section = nomenclature
    name = 'room_name_plural'
    verbose_name = "Plural name of rooms throughout the system."
    default = "Labs"
    required = True

@global_preferences_registry.register
class StorageName(StringPreference):
    section = nomenclature
    name = 'storage_name'
    verbose_name = "Name of storage location throughout the system."
    default = "Cabinet"
    required = True

@global_preferences_registry.register
class StorageNamePlural(StringPreference):
    section = nomenclature
    name = 'storage_name_plural'
    verbose_name = "Plural name of rooms throughout the system."
    default = "Cabinets"
    required = True

@global_preferences_registry.register
class UseLocationName(StringPreference):
    section = nomenclature
    name = 'uselocation_name'
    verbose_name = "Name of in-use location throughout the system."
    default = "Setup"
    required = True

@global_preferences_registry.register
class UseLocationNamePlural(StringPreference):
    section = nomenclature
    name = 'uselocation_name_plural'
    verbose_name = "Plural name of in-use locations throughout the system."
    default = "Setups"
    required = True

from datetime import timedelta

# @global_preferences_registry.register
# class CheckHighPriorityWeeks(DurationPreference):
#     section = check
#     name = 'check_highpriority_weeks'
#     verbose_name = "Number of weeks unchecked when item becomes high priority."
#     default = timedelta(weeks=23)
#     required = True

@global_preferences_registry.register
class CheckHighPriorityInWeeks(IntegerPreference):
    section = check
    name = 'check_highpriority_inweeks'
    verbose_name = "Number of weeks unchecked when item becomes high priority."
    default = 24
    required = True

@global_preferences_registry.register
class CheckMediumPriorityInWeeks(IntegerPreference):
    section = check
    name = 'check_mediumpriority_inweeks'
    verbose_name = "Number of weeks unchecked when item becomes medium priority (up to high priority duration)."
    default = 12
    required = True

@global_preferences_registry.register
class CheckHighPriorityStorageInWeeks(IntegerPreference):
    section = check
    name = 'check_highpriority_storage_inweeks'
    verbose_name = "Number of weeks unchecked when item in storage becomes high priority."
    default = 48
    required = True

@global_preferences_registry.register
class CheckMediumPriorityStorageInWeeks(IntegerPreference):
    section = check
    name = 'check_mediumpriority_storage_inweeks'
    verbose_name = "Number of weeks unchecked when item in storagebecomes medium priority (up to high priority duration)."
    default = 24
    required = True