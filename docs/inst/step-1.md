---
description: 'Obtain transport files. Unzip and place in transport folder. Import transports using STMS transaction.'
---
# Step 1 - Obtain and import the transport files

## 1. Contact Nype

Contact Nype's representative to obtain the zip file with transports.

## 2. Unzip and place files in your transport folder
Unzip the cofile and data files, and place them in the respective folder on your application server.

## 3 Perform the import
Using SAP Gui transaction **STMS** import the transport to your system. 

  - Please specify the target client as the transports contain client specific configuration like Authorization Roles.
  - Please mark the option "Overwrite originals" and "Ignore Invalid Component Version"

Recommended order:

1. FT-Core.zip
2. FAU-Report.zip
3. FAU-Plugin.zip
4. FAU-Users.zip
5. FT-ASIS-Main.zip
6. FT-ASIS-Connector.zip
7. FT-Import.zip
8. FT-Roles.zip
9. FT-Users.zip (Requires FT-Roles.zip)
10. FRT-Report.zip (Requires FT-Roles.zip)


[![](res/stms.png)](res/stms.png)