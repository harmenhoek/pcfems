Harmen Hoek<br />
December 2020<br />
Current version: 0.1 (december 2020) <br />
Created for: Physics of Complex Fluids, University of Twente.<br />
Current development phase: beta-testing, not usable.

## About

Pcfems is the equipment management system for Physics of Complex Fluids at University of Twente. The system allows for tracking equipment in a web-based application that is accessible on desktop and mobile. QR-code labeled equipment can be scanned with the integrated scanner. Users can assign equipment to a location (experimental setup) or user. Each item has a logbook, a history view and flag functionality for reporting problems. Staff-assigned users can add new items, delete items and see user activity. 

The application is built in Django with (currently) a SQLite database. 

### Full feature list
- Searchable database with equipment
- Detail page for equipment with image support
- Responsive design for desktop and mobile usage
- Integerated Javascript QR-code scanner.
- Logbook with file uploads.
- Assign functionality to track location and user of equipment
- User login, profile, password forget
- Additional staff functionality including full edits, delete, user management, user activity overview, full item history.

### Third-party integrations
- activity_log
- simple_history
- crispy_forms
- qr-scanner
- qrcode-6.1
- reportlab.pdfgen
- ekko-lightbox 5.3.0

## Workflow

### Create an account
It is not possible to create your own account. Contact a staff member to request an account. Was your account already created, but you don't have a password? Then press `Forget password?` on the login page, and use your institution email address to reset your password.

### Change password
To change your password, logout and press `Forget Password?` to reset your password using your email.

### Scanning item on mobile
Scanning an item that is labeled with a QR-code. <br>
QR codes are slug-based, containing only a unique ID. This means that items need to be scanned inside the application, and not with any other QR-code scanner. Any browser-recognized camera can be used, including desktop webcams (although impractical).

To scan an item, a user has to be logged in. 
1. Press `Scan` in the main menu bar.
SCREENSHOT
2. If scanning an item for the first time, a popup asks to allow the website to use the camera. Accept this. To prevent this message in the future, allow the website to always use the webcam, see SECTIOn below.
3. Point the camera at the QR code. It is not needed to align the code perfectly with the field-of-view. Once recognized you will be automatically forwarded to the detail page of that item. If the code is not instantly recognized, move the camera in and out. Alternatively, search the database for the item ID below the QR-code.

### Searching item on desktop
To search for an item, a user has to be logged in.
1. On the home screen of the application, enter the search term in the Search-bar in the top-right corner. All fields will be searched and results will be shown instantly. Also item fields that are not shown will be searched (e.g. purchased date and serial number).
SCREENSHOT
2. To search or filter a specific field, use the searchbar or selection list at the top of the field column.

### Assign item to or return to storage
When an item changes location, i.e. either moves from storage to a user or experimental setup, it has to be assigned to the new user or location. To assign an item, select `Assign To` on the item detail page. If an item is currently in use, the assignment can be changes by selecting `Change Assign To`. Next, select the new location and optionally the user and date of return and press `Assign`. The item availability will change from `Available` to `In use`.

If an item is to be returned to storage, simply press `Return to Storage`. The item availability will change from `In use` to `Available`.

### Update an item
If basic item details are missing or incorrect, the item can be updated by selecting `Update` from the `Actions` menu. Here the description and images can be updated. Up to 2 images can be added to each item. If more images need to be added, add a log to the item (see <a href="#add-or-update-a-log">Add or update a log</a>)<br>

All users can update the description and images. Staff members can update all the item details ((see <a href="#staf:-update-an-item-fully-or-delete">Staff: update an item fully or delete</a>).


### Add or update a log
Logs are meant to add time-specific information to an item, such as current problems or custom manuals. To add a log, select `Add log` on the item detail page. Add the log in the log-field and optionally add up to 2 attachments (any type of file) and set a custom names to displayed for the files in the log. If no name is entered, the filename will be displayed. 
Logs are meant to add time-specific information to an item, such as current problems or custom manuals. To add a log, select `Add log` on the item detail page. Add the log in the log-field and optionally add up to 2 attachments (any type of file) and set a custom names to displayed for the files in the log. If no name is entered, the filename will be displayed.<br />

To update or delete a log, select `Update` or `Delete` next to the log. You can only update or delete your own logs.


### Flag an item
An item can be flagged if an action is required. Examples of flags are 'item needs repair', 'item needs cleaning' and 'item is missing'.<br>
To add flag, select `Flag` on the item detail page, and select the flag, and save. Staff members can add, update or delete flag options in the manage overview (see 'Staff: manage users, flags, categories, monitor user activity' below.)

**Note**: In the current version the flag only shows up in the Flag overview in the staff manage overview. No notifications are send.  


### Staff: add a new item
To add a new item to the database, select `Add item` from the `Admin` menu in the header. Fill in at least the mandatory fields marked by a '*'. Press `Add` to add the item. In the background several fields are added automatically, including the unique item ID (or slug).

**Note:** In the current version it is not possible to add a category when adding a new item (no widget wrapper). Categories ca be managed in the manage overview (see 'Staff: manage users, flags, categories, monitor user activity' below.)

### Staff: update an item fully or delete

### Staff: manage users, flags, categories, monitor user activity


## Q&A

#### Q: Can a staff member see my password?
> No, you password is encrypted and cannot be viewed by anyone.

#### Q: I am trying to reset my password, but I am not receiving an email.
> Either your account is set to *inactive* by a staff member, or your no account is registered to your email address. You don't receive an error message when requesting a new password, to prevent hackers from obtain email addresses using this functionality. Contact a staff member for more information.

#### Q: I want to Assign an item to a new location or user.
> Only staff members can add locations or users, please contact a staff member.

#### Q: I want to Assign an item to an external user or group.
> A staff member can add a user (or group) and set this user to inactive. Now this user or group can be assigned items to. In the future a separate 'Add to external' feature might be added.  

#### Q: I have feedback or questions about the system.
> Please contact Harmen.


IN FUTURE: assign to other group.

## In-dept
User types,
Categories
Locations
Assingin
How does all this work in the backend?

#### Searching item on desktop

#### Add new item

#### User types

## User tips
ADD ITEM TO HOMEPAGE
ALLOW CAMERA ALWAYS

## Screenshots (version 0.1)


Known bugs

RESOLVE BUG: when adding/updating item to warranty and ONLY exp date is given, not service date.

TODO
- bulk import csv
- Scan log 
- TODO: mandatory fields when adding / updating
- hidden search fields
wha




## Changelog

### Release v0.1 (not released yet)
Changes here

2020-01-05
- Added bootstrap_datepicker_plus for createview.
- Installed bootstrap via pip, loaded into base.html, commented the old links, beware this works perfectly everywhere.
- Updated manage: locations (setup, lab and cabinets), categories and flags.
- DataTables to item detail page: logbook and item history

2020-01-06
- Deprecated qrgenerator.html, now in-view QR generation (using qrcode-6.1) with PIL processing for caption. Now HttpResponse of image insteafd of render html.
- Created qrbatchgenerator to create batch pdf files with qr codes using reportlab.pdfgen and io.

2020-01-07
- @login_required, @staff_member_required fixed for all views. Only about and login now accessible without login.
- date selector in StaffUpdateView and AssignForm.
- Help texts in forms.
- Manage interface: open flags (with resolve), assigned items (with return) and items under warranty (with remove warranty) overview added.
- Success messages on all Manage pages when creating, updating or pressing a single action button.

2020-01-08
- In manage openflags, flagged_by and flagged_on is retrieved by querying the item history. 
- Added success messages to ems views. Not fully tested.
- Added flag functionality to item-detail: show current flag and button to flag / resolve flag.
- Added Lightbox to detail page (ekko-lightbox 5.3.0). When default image (now SETTING), no lightbox.
- Hide Home and Scan when logged out


## History

Whenever a model instance is saved a new historical record is created.