# Equipment Management System
Current version: 0.1 (November 2020)

## General description

### Workflow

#### Scanning item on mobile

#### Searching item on desktop

#### Add new item

#### User types

## TO DO

### Insert form
- Add related widget wrapper to add categories on the go (http://dashdrum.com/blog/2012/07/relatedfieldwidgetwrapper/)
- Auto-complete for faster entering?
- Date selectors
- Extra information around to guide (widgets to custom form https://docs.djangoproject.com/en/3.1/ref/forms/fields/)
- Multi-add option
- Import of csv

### Detail page
- Timeline of recent activity of item
- On side the quick actions: Add files, Edit item, Claim
- Export to
- Refined item history
- Proper flagging
- Image lightbox
- Filter Notes and History. Notes e.g only with attachments, or only <1 month old.

### Custom admin interface
- Allow to add categories, labs, etc.
- Multi-image support, allow users to upload images and manual(s).
- See soon due service dates and flags
- Show users, add users, show items in use, items per user, statistics.

### User page
- Clickable username to page
- Show items in use by this person

### Major functionality
- QR code generator for new items. When adding, ask to enter pre-printed qr code, or scan it. Show a selection box with pre-printed QR-codes. Only those just printed can be added to the system.
- Admin environment: see all logs, add categories, etc. Add link to menubar. See recent activity. See flags in overview.
- Password forget with emails
- Continue Django Docs.
- Header prevent collapse of Scan
- Header dropdown for user with Profile and Log Out

### For future
- New model for images. Link images to model. How to add this to history as well.

## Changelog

### Release v0.1 (not released yet)
Changes here


## History

Whenever a model instance is saved a new historical record is created.