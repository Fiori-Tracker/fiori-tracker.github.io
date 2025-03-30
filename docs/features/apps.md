# FT Applications

## Introduction

With the help of the application "FT Applications," you can store the records of all your Fiori launchpad-enabled applications. The list of all apps stored in "FT Applications" serves as a directory of all applications in the project scope. Application records are kept as [Specification records](../specification-records.md) and referred to with an "App ID." The records serve as a single point of truth for application information in your project (project's "SAP Fiori library"). A major benefit is having custom and extended app records in one central place.

[![](res/apps.gif)](res/apps.gif)

## Attributes of App Specification record

Fiori Tracker keeps the following attributes for an app entry:


| Name      | Description                                                                                                             |
|-----------|-------------------------------------------------------------------------------------------------------------------------|
| Id        | App identifier. For SAP standard application, we recommend the use of application id from Fiori Apps Library        |
| Name      | The name of the application                                                                                             |
| Tile tile | The name to be set for Fiori Launchpad tile                                                                           |
| Area      | Functional area chosen from the list of areas in your project. The list is configurable.                             |
| Type      | Type of the application. Fiori Tracker comes with predefined application types. The list is configurable.             |
| Created   | The date on which the application Specification entry was created.   It is the date of including the app in the project scope. |
| Modified  | The date on which the user has changed the attributes of app.   |

## Configuration

To configure Fiori Tracker core use SAP Gui transaction **ZFTADMIN**:

![](res/zftadmin.png)

### Modify config

The "Modify config" function allows you to set configuration parameters.

| Key                          | Value     | Description                                                                                                                                                                    |
|------------------------------|-----------|------------------------------------------------------------------------------|
| INCOMP_HIDE                  | **TRUE** | When set to TRUE the version compatibility warning will not show |


### Area codes

The "Modify area codes" function allows you to define the names of the areas used in your project.

### Application types

Allows you to modify or add the application types.

### Application properties

Allows you to choose additional properties. Attributes can be switched on and off depending on your project needs.

| Key | Description  |
|--|--|
| GIT_REPO | Custom app or extension git repository name | 
| UI5_COMP_NAME | UI5 component name | 
| DOCS | Link to technical documentation nof the app| 
| TR_PACKAGE | Transport package containing all the app's objects | 
| MAIN_ODATA_SRV | Main oData service | 
| OriginalAppId | In case of extended app the original App ID | 
| OriginalAppName | In case of extended app the original App name | 
| IsLighthouse | Is the application Lighthouse| 
| IS_MIGRATED_BAS | Was the app migrated to SAP Business Application Studio already | 
| GOLIVE_ON | Date on which the app went live |
| IS_MARKED_AS_DELETED | Is the app deleted  | 
| CAN_BE_STARTED_FROM_FLP | Can the user start the app from Fiori Launchpad |
| DESC1 | Custom attribute 1 | 
| DESC2 | Custom attribute 1 |
| DESC3 | Custom attribute 1 | 
| DESC4 | Custom attribute 1 | 

### Relations

Allows you to choose available relations. 