# Step 5 - Set the parameters for activation key, log mode and target system

1. Go to SAP Gui transaction `ZFACENADMIN` and press the button labeled `2. Edit configuration`. 
Pressing the button will open a maintenance view for table `ZNYPEFACEN_SC`:

[![](res/fa-conf.png)](res/fa-conf.png)

2. In the configuration table add the following entries:

|Config key|Config value|
|--|--|
|ACTIVATION_KEY|*Report key provided by Nype's representative*|
| LOGMODE                      | **FULL** |

3. Go to SAP GUI transaction `ZFAMANADMIN`. Entering transaction will initialize the plugin configuration.

[![](res/faman-conf.png)](res/faman-conf.png)

4. Press the button labeled: *1. Edit configuration.* Pressing the button will open a maintenance view for table `ZNYPEFAMAN_SC`:

[![](res/faman-conf-tab-for-full-inst.png)](res/faman-conf-tab-for-full-inst.png)

5. In the configuration table add the entry for Plugin activation key:

|Config key|Config value|
|--|--|
|ACTIVATION_KEY|*Plugin key provided by Nype's representative*|
|LOGMODE|FULL|

See also: 

- [How to get the SAP system installation number](installation-number.md)
- [How to prepare the RFC destination pointing from Central system to Managed system](rfc.md)
