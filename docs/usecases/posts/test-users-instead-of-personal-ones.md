---
date: 2020-02-14
slug: "SPS03/test-users-instead-of-personal-ones"
categories:
  - Project management
---
# Using test users instead of personal ones 

SAP Fiori applications are [build with specific user roles in mind](https://experience.sap.com/fiori-design-web/design-principles/#rolebased), so testing must be aligned accordingly.

<!-- more -->
Conducting role-based testing with test users who have the relevant roles is essential. This approach also helps to avoid issues that may arise from using project members' personal accounts, such as:

- Missing SAP functional configuration, parameterization, or user-specific test data
- Inconsistent results due to varying application behavior per personal user ("it works for me!")

To facilitate this approach Fiori Tracker offers an app for centrally maintain list test user records. Test user records are linked directly with roles and indirectly with catalogs and apps.