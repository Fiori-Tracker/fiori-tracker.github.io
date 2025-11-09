# Your questions, answered

## Fiori Tracker (general)

<div class="nype-faq" markdown>


??? faq "Does Fiori Tracker send any data (statistics) to the outside servers (what is the security model)?"

    Fiori Tracker is not sending any data to outside servers. Fiori Tracker does not need external access, and many users run it on installations that do not have external access. All code is in ABAP, meaning that it is fully transparent and available for inspection.

??? faq "What are the prerequisites/minimal requirements for installation?"

    The minimal requirement is any SAP system with GAP Gateway (software component SAP_GWFND) on SAP NetWeaver version at least 7.52 ([see details](inst/min.md))

??? faq "Will the Fiori Tracker release 2020 work on my S/4HANA system on a different release (1610, 1709, 1809, 1909, 2021, 2022, 2023)?"

    Yes. Fiori Tracker release numbering is independent of SAP release numbering. Fiori Tracker release 2020 is compatible with SAP S/4HANA releases from 1610 to 2023. Refer [Minimal requirements](inst/min.md) for more details.

??? faq "What details do you need for troubleshooting the issues?"

    Please send the screenshots of the application running in Chrome with URL and "Developer tools" console.

    Screenshot from respective SAP Gateway system from SAP Gui menu: System->Status SAP System Data -> Details.

??? faq "How to de-install Fiori Tracker components?"

    To de-install Fiori Tracker components, please perform the reverse of the installation steps in the reverse order. For import transports steps perform the deletion of the objects from the component's transport package.

??? faq "Why would I need a dedicated app instead of the shared Excel spreadsheet or Atlassian Confluence page?"

    App records kept in the spreadsheet cause many challenges. Here are the most important ones:

    - Unauthorized, accidental modification causing inconsistencies
    - Lack of history and origin of changes
    - Duplication
    - Lack of 1 to N relation maintenance

    See ["The challenges of storing Fiori content records in the spreadsheet"](usecases/posts/spreadsheet-challenges.md) for more details.

??? faq "How to get the SAP system installation number?"

    Please check the [detailed description](inst/installation-number.md).

</div>

## Fiori App Usage Report

<div class="nype-faq" markdown>

???+ faq "Is there any way that I can pull the historical data?"

    The data is collected when the Fiori App Usage Plugin is active for the user, so there is no way to pull the historical data.

??? faq "What is the architecture of the solution?"

    Please find the details on the [Architecture page](fiori-app-usage/architecture.md).

??? faq "How is the solution deployed?"

    Fiori App Usage Report is deployed by importing the transports. Please find the details on the [Deployment page](fiori-app-usage/deployment.md).

??? faq "How much time does it take to implement the Fiori App Usage and start collecting the usage records?"

    You can set up and start using Fiori App Usage in a couple of hours. We will send you descriptions that will guide you through all the required steps. Should you encounter any problem, you can reach Fiori App Usage team on the support Discord channel or ask the team for a screen-sharing session.

??? faq "Can I use my roles instead of the ones provided in Fiori App Usage transport requests?"

    Yes. [See how to create or extend an existing role](fiori-app-usage-plugin/extend-existing-role.md).

??? faq "Should we install Fiori App Usage Report on SAP Solution Manager?"

    SAP Solution Manager is a very good choice when it comes to using Fiori App Usage Report and Fiori Tracker suite tools when your main landscape can get temporarily offline (upgrades and other maintenance activities). The only reason we do not encourage our users to use SAP Solution Manager is that most of the installations are on NetWeaver below 7.52 while Fiori Tracker Suite component need at least NetWeaver 7.52. If your SAP Solution Manager is on 7.52 then it is a perfect place for installation.

??? faq "Do you have a demo of the application?"

    We can arrange a call to demo Fiori App Usage Report on our systems. Please let us know using [this form](https://help.fioriappsusage.org/offer/) if you would like to have a call. We will send the timing proposition.

??? faq "What are all roles needed for manager and user?"

    Please check the [summary](inst/roles.md).

??? faq "What is the Fiori App Usage impact on applications and system performance?"

    Fiori App usage impacts overall system performance as little as possible. See the details in [Fiori App Usage performance influence section](fiori-app-usage/performance.md).

??? faq "Why should we use a third-party solution instead of waiting for the same function delivered by SAP out of the box?"

    Any solution to the application usage reporting problem will require identifying the applications covered by the project. As the Fiori App Usage Report's key aspect is the identification, you can start tracking the app usage with the Fiori App Usage Report and leverage the same app identification records if the standard out-of-the-box solution will be developed.

</div>
