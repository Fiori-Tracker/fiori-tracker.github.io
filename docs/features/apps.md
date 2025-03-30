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