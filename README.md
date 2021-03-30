## About

PCFEMS is the equipment management system for Physics of Complex Fluids at University of Twente. The system allows for tracking equipment in a web-based application that is accessible on desktop and mobile.
QR-code labeled equipment can be scanned with any QR-code scanner. Users can assign equipment to a location (experimental setup). Each item has a logbook, a history view and flag functionality for problem reporting. Staff-assigned users can add new items, delete items, manage categories, flags and locations, see user activity and export items for label printing via the manage interface.  

### Definitions

#### Label
Each item is physically labeled. The label contains the QR-code, tracking requirements and basic item information. Multi part items are labeled separately but refer to the same item.

#### Tracking
There are two types of items. Items that **require tracking** and items that **don't require tracking**. <br>
Items that require tracking need to be assigned to a new location (and user) when the item is moved, and stored at a specific location when unassigned. The exact location is always known in the system. <br>
Items that don't require tracking can be moved around freely without recording its location, but are in the system for logging and flagging purposes.
<table>
<tr>
<td style="width:100/3%;"><img src="screenshots/tracking.PNG">Item label for item that <b>requires tracking</b>
<td style="width:100/3%;"><img src="screenshots/notracking.PNG">Item label for item that <b>doesn't require tracking</b>
</tr>
</table>

#### Status
An item can have one of the following status: **in use**, **available** or **no tracking**.<br>
Items that are in use are assigned by a user to a specific location. <br>
Items that are available are not in use and can be found at the set storage location.<br>
For items that are not tracked the location and user is not known.
<table>
<tr>
<td style="width:100/3%;"><img src="screenshots/status_inuse.png">Item status <b>in use</b>
<td style="width:100/3%;"><img src="screenshots/status_available.png">Item status <b>available</b>
<td style="width:100/3%;"><img src="screenshots/status_notracking.png">Item status no <b>tracking</b>
</tr>
</table>

#### Assigning
Assigning is designating an item to a specific location, and optionally a user. Only items that are tracked can be assigned.

#### Flagging
Flagging is marking an item for attention or treatment in a specified way. An item can for example be flagged as missing, broken or due for inspection.

#### Location
The location of the item is either **lab + experimental setup** when in use (blue badge) or **lab + cabinet** (yellow badge) when in storage, thus available.

#### Staff
A staff member is an EMS user with extra functionality inside EMS. Extra functionalities of staff members include adding new items and users, updating all item details, removing items and adding new categories, locations and flags.

### Third-party integrations
- activity_log
- simple_history
- crispy_forms
- ekko-lightbox 5.3.0

## Workflow

### Login
Accounts can only be created by existing staff members inside the system. Users with an account but no password can press `Forget password?` on the login page to reset their password.

### Equipment overview & item search
The main view of the app gives an overview of all the items. The table can be searched real-time with the global search bar in the top-right, or using the field specific search options in the table. Clicking an item will redirect to the item-detail page.


In the top menu bar you can find links to the overview of storage locations, admin options (only visible to staff) and profile options.

<table>
<tr>
<td><img src="screenshots/version1_0/overview_explained.jpeg">Equipment overview (main view).
</tr>
</table>


### Scanning item on mobile
Scanning an item that is labeled with a QR-code. <br>
The QR codes contain a unique URL referring to the item detail page plus a label version number to check wether the item is still up to date.
Any QR-code scanner can be used to scan the QR-code. If logged in the user will be redirected to the item-detail page.
<table>
<tr>
<td><img src="screenshots/version1_0/qrcodescan_explained.jpeg">QR-code scanning.
</tr>
</table>


### Searching item on desktop
To search for an item, a user has to be logged in.
1. On the home screen of the application, enter the search term in the Search-bar in the top-right corner. All fields will be searched and results will be shown instantly. Also item fields that are not shown will be searched (e.g. purchased date and serial number).
2. To search or filter a specific field, use the searchbar or selection list at the top of the field column.

### Item detail-page & assign an item
The item-detail page shows all the details of the item, the item-specific logbook and history and shows the item actions.

The main purpose of the EMS is keeping track of the whereabouts of equipment. Tracking a piece of equipment is done by assigning an item to a specific location and optionally a user when in use.
To assign an item to a new location:
1. Press `Assign To` or `Change Assign To` in the `Quick Actions` menu;
2. Select the new location and optionally the user and return date and press `Assign`.

The item availability will change from `Available` to `In use`.

If an item is to be returned to storage, simply press `Return to Storage`. <br>
The item availability will change from `In use` to `Available`.

<table>
<tr>
<td><img src="screenshots/version1_0/item-detail_explained.jpeg">Item-detail page.
</tr>
</table>


### Update an item
If basic item details are missing or incorrect, the item can be updated by selecting `Update` from the `Actions` menu. Here the description and images can be updated. Up to 2 images can be added to each item. If more images need to be added, add a log to the item.<br>

All users can update the description and images. Staff members can update all the item details (see below).

### Add or update a log
Logs are meant to add time-specific information to an item, such as current problems or custom manuals. To add a log:
1. Select `Add log` on the item detail page. Add the log in the log-field and optionally add up to 2 attachments (any type of file) and set a custom names to displayed for the files in the log. If no name is entered, the filename will be displayed.

To update or delete a log, select `Update` or `Delete` next to the log. You can only update or delete your own logs.


### Flag an item
An item can be flagged if an action is required. Examples of flags are 'item needs repair', 'item needs cleaning' and 'item is missing'.<br>
To add flag, select `Flag` on the item detail page, and select the flag, and save. Staff members can add, update or delete flag options in the manage overview (see 'Staff: manage users, flags, categories, monitor user activity' below.)


### Staff: add a new item
To add a new item to the database, select `Add item` from the `Admin` menu in the header.

The available fields are:
- **Title** - A short 25-character title describing what the item is. Be as general as possible, but add specific details if space allows to differentiate it from other items. Good titles are: 15 MHz function generator, DC power supply 0-20V, 40MHz analog oscilloscope and 4K USB camera.
- **Category** - A category bins items that are similar and makes searching for similar items easier. For example when searching for a power supply selecting the Power supplies category shows all power supplies (AC, DC, HV). Find a category that is most specific. For example a multimeter might fit in the General electronics category, but is better binned in the Multimeters category. If you are sure an item might form a new category with other items, this category can be added in the manage environment (section 4.4).
- **Brand** - The brand of the item. If the item is homemade, use Homemade. If unknown, use Unknown.
- **Model** - The model of the item. If unknown or homemade, use Unknown. Does the item consist of multiple parts
(e.g. a proprietary power supply), comma separate the models in this field.
- **Serial** - The serial number of the item. Does the item consist of multiple parts (e.g. a proprietary power supply), comma separate the serial numbers in this field.
- **Parts** - The number of separate parts of the item. For example, a laser might consist of the laser itself, a power supply and a remote control. All these 3 parts can be disconnected and all mandatory for the laser to work. This item will thus have 3 parts.
- **Description** - Add as many details about the item as possible: text written on the item, specs or even descriptions and spec sheets copied elsewhere online.
- **Storage Location** - Find a storage location with similar items and verify space is available here to storage it. Each shelf in a cabinet is a separate storage location. New locations can be added in the manage environment (section 4.4).
- **Image** and **Image2** - Add images of the front and back (connections) of the item. Take photos with a neutral background if possible. More images can be added to logbook if needed.
- **Purchased by**, **Purchased on** and **Purchased price** - Optional fields to specify who bought the item, when and at what price.
- **Warranty**, **Warranty expiration** and **Next service date** - Optional fields for newly purchased items to specify any warranty information. Warranty items will show up in the manage environment separately sorted by the next service date.

### Staff: update an item fully or delete
Contrary to normal users, staff can update all fields of an item. To update an item select `Full update` from the `Actions` menu of the item detail page when logged in as a staff member.

### Print QR-codes
Printing QR codes is a 2-step process: exporting the data from EMS followed by importing the data and printing the labels with the Dymo software.
1.  Exporting the data can be done in the manage-environment of EMS. Go to `Admin` → `Manage` → `Export`. Select the ID range of items you wish to export (e.g. 10-50, for labels PCF0010-PCF0050), and press Export. 2 csv-files will be exported named `export_tracking.csv` and `export_notracking.csv`.
2. Open the Dymo software `DYMO Connect for Desktop` (tested on Windows 10 with DYMO Connect for Desktop 1.3.2). Open the template `pcfems_labels_version20210217_tracking.dymo` and select `Import data` from the top of the screen. Select the csv file `export_tracking.csv` that was just exported, verify you selected the tracking file. Once imported make sure the label size shown in the bottom of the screen matches the labels currently in the printer, and press `Print` to print the labels.
3. Repeat step 2 for the no-tracking items. Use `export_notracking.csv` in combination with `pcfems_labels_version20210217_notracking.dymo`.

The Dymo LabelWrinter 450 Turbo was used when writing this manual. Standard label size: Medium Multipurpose Labels 30335 | LW 32x57mm SKU: S0722540.

### Manage environment
The manage environment of EMS allows staff members to see extra statistics and manage the system. The manage environment can be found under `Admin` → `Manage`.

#### Overview
In the overview tab you can find the items that are currently flagged, the currently assigned items and items under warranty. Items that are flagged need attention and flags can be resolved immediately from this view.

#### Users
Adding users to EMS can be done from this view. There are 3 types of users: general users (don’t have access to any of the staff functionalities), staff (can add, remove and fully edit item plus have access the the manage environment) and admins (have access to the back-end, cannot be added through the EMS front-end).

Users cannot be deleted from the system, as their name can still be used throughout the system. Instead a user can be set to `Inactive`. Inactive users can no longer login or reset their password.

Passwords cannot be reset through this interface. A user reset their password with their known email address using the `Forget Password?` functionality on the login page.

#### Activity
Under development. Currently shows all the raw page request.

#### Flags
Flags can be edited and added here. A flag has a name, description and icon. Icons can be found in the Font Awesome library.

#### Categories
Categories can be edited and added here. Make sure a category is unique and does not overlap with other categories.

#### Locations
Each item in EMS is linked to a location. Each location is build up out of 2 parts:
1. Lab
2. Setup or Cabinet

When an item is in use (assigned to a user) the location is Lab + Setup, when the item is in storage the location is Lab + Cabinet.
On this page you can add Labs, Setups and Cabinets. EMS takes care of combining these into locations.

#### Export
Here you can export items to csv-files. See above.



## Screenshots (version 1.0)
<table>
    <tr>
        <td><img src="screenshots/version1_0/login.png">Login</td>
        <td><img src="screenshots/version1_0/overview.png">Home view</td>
    </tr>
    <tr>
        <td><img src="screenshots/version1_0/search_thermometers.png">Item search</td>
    </tr>
    <tr>
    <td><img src="screenshots/version1_0/cabinetview_ME106_07_03.png">Cabinet overview</td>
    <td><img src="screenshots/version1_0/userview_harmenhoek.png">Userview page</td>
    </tr>
    <tr>
        <td><img src="screenshots/version1_0/detailview_available.png">Detail page (item available)</td>
        <td><img src="screenshots/version1_0/detailview_inuse.png">Detail page (item in use)</td>
    </tr>
    <tr>  
        <td><img src="screenshots/version1_0/logbook.png">Logbook overview</td>
        <td></td>
    </tr>
    <tr>
        <td><img src="screenshots/version1_0/additem.png">Adding new item (staff only)</td>
        <td><img src="screenshots/version1_0/updateitem.png">Updating an item</td>
    </tr>
    <tr>
        <td><img src="screenshots/version1_0/manage_openflags.png">Manage interface (staff only)</td>
        <td><img src="screenshots/version1_0/manage_locations_cabinets.png">Manage locations interface (staff only)</td>
    </tr>

</table>
