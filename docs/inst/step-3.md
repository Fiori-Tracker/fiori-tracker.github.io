---
description: 'Enable OData service: Generate runtime objects in SEGW, add service to catalog in /n/IWFND/MAINT_SERVICE, add system alias to ICF node and activate.'
---
# Step 3 - Enable oData service

To enable oData service complete the steps described below. 

!!! info

    Follow these steps for each project / service one by one, not simultaneously. 

## 1. Generate Runtime objects in transaction SEGW

1.1. Start SAP Gui transaction `SEGW`<br>
1.2. Using the menu `Project` > `Open` - Open the `service name_projectname`.

[![](res/segw.png)](res/segw.png)

1.3. Go to Change mode and choose function `Generate` (you will be prompted for transport and your user must be registered as developer)

[![](res/segw_gen.png)](res/segw_gen.png)

## 2. Add the Service to Service Catalog

2.1 Start SAP Gui transaction `/n/IWFND/MAINT_SERVICE`.

2.2 Find entry with the `service name`.

If the entry is present then move to sub-step 3 (Add system alias to ICF node), in not, please execute the following steps:

2.3 Click on the `Add service` button.

2.4 Provide System Alias: LOCAL and External Service Name as the `service name`.

2.5 Select the record with the `service name` and click on the Add selected services button.

## 3. Add system alias to ICF node

3.1 In `/n/IWFND/MAINT_SERVICE`, choose the `service name`.

3.2 If ICF node is green and alias is present (like below) then the procedure is completed.

[![](res/maint-service.png)](res/maint-service.png)

If not, please execute the following steps:

3.3 Choose `Add system alias`, `New entry` and in column in *Service Doc. Identifier* type `service name_0001`, in *SAP System Alias* type "LOCAL" and in column *Default System*, mark the check-mark.

3.4 Click on `ICF node` button and from drop down choose `Activate`

[![](res/maint-service-icf.png)](res/maint-service-icf.png) 

3.5 Click on `Load Metadata` button

[![](res/maint-service-meta.png)](res/maint-service-meta.png) 