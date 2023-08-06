# Netbox Software Plugin

A plugin designed to faciliate the storage of site, circuit, device type and device specific software within [NetBox](https://github.com/netbox-community/netbox)

## Features

* Store software against the following NetBox models:
   - Circuits
   - Devices
   - Device Types
   - Sites

* Upload software to your NetBox media/ folder or other Django supported storage method e.g. S3
* Supports a wide array of common file types (bmp, gif, jpeg, jpg, png, pdf, txt, doc, docx, xls, xlsx, xlsm)
* Store links to external URL's to save duplication of remote software


## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     3.2+       |      0.5.0     |


## Installation

A working installation of Netbox 3.2+ is required. 3.4+ is recommended.

#### Package Installation from PyPi

Activate your virtual env and install via pip:

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-software
```

To ensure the Netbox software plugin is automatically re-installed during future upgrades, add the package to your `local_requirements.txt` :

```no-highlight
# echo netbox-software >> local_requirements.txt
```

#### Enable the Plugin

In the Netbox `configuration.py` configuration file add or update the PLUGINS parameter, adding `netbox_software`:

```python
PLUGINS = [
    'netbox_software',
]
```

(Optional) Add or update a PLUGINS_CONFIG parameter in `configuration.py` to configure plugin settings. Options shown below are the configured defaults:

```python
PLUGINS_CONFIG = {
     'netbox_software': {
         # Enable the management of device specific software (True/False)
         'enable_device_software': True,
         # Location to inject the software widget in the device view (left/right
         'device_software_location': 'left',
     }
}

```

(Optional) Add or replace the built-in software Type choices via Netbox's [`FIELD_CHOICES`](https://netbox.readthedocs.io/en/feature/configuration/optional-settings/#field_choices) configuration parameter:

The colours that can be used are listed in the Netbox CSS netbox-light.css:

(https://github.com/netbox-community/netbox/blob/develop/netbox/project-static/dist/netbox-light.css)

The bg- must not be specified in the configuration.
Here are a few examples from the CSS:

* bg-indigo = #6610f2 --> 'indigo'
* bg-blue = #0d6efd --> 'blue'
* bg-purple = #6f42c1 --> 'purple'
* bg-pink = #d63384 --> 'pink'
* bg-red = #dc3545 --> 'red'
* bg-orange = #fd7e14 --> 'orange'
* bg-yellow = #ffc107 --> 'yellow'
* bg-green = #198754 --> 'green'
* bg-teal = #20c997 --> 'teal'
* bg-cyan = #0dcaf0 --> 'cyan'
* bg-gray = #adb5bd --> 'gray'
* bg-black = #000 --> 'black'
* bg-white --> 'white'

```python
FIELD_CHOICES = {
    'netbox_software.DocTypeChoices.device+': (
        ('mysoftware', 'My Custom Device software Type', 'green'),
    )
}
```

#### Apply Database Migrations

Apply database migrations with Netbox `manage.py`:

```
(venv) $ python manage.py migrate
```

#### Restart Netbox

Restart the Netbox service to apply changes:

```
sudo systemctl restart netbox
```

#### Re-index Netbox search index (Upgrade to 3.4 only)

If you are upgrading from Netbox 3.2 or above to Netbox 3.4, any previously inserted software may not show up in the new search feature. To resolve this, re-index the plugin:

```
(venv) $ python manage.py reindex netbox_software
```

