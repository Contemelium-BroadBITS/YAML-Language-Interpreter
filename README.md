# 1. Introduction
This interpreter serves as a bridge between rule declarations written in YAML format and executable Python code within OpExpert. It supports five fundamental operations crucial for setting rules within the OpExpert environment: Condition, Execution, Function, Integration, and Module. Each operation corresponds to a specific aspect of rule definition and execution.

- Condition: Specifies the conditions under which a rule should be triggered or applied.
- Execution: Defines the actions or tasks to be executed when a rule's conditions are met.
- Function: Allows users to define custom functions or methods to be used within rule execution.
- Integration: Facilitates the integration of external services or systems into rule execution.
- Module: Enables the organization and modularization of rule components for better management and reusability.

<br>

***
*[Section 3.1](#31-formatting-your-yaml-script) of this documentation provides detailed instructions on how to format the YAML file correctly to define rules using these supported operations. By adhering to the specified format, users can seamlessly translate their rule definitions from YAML into Python code, ensuring compatibility and effectiveness within the OpExpert environment.*

<br>
<br>
<br>

# 2. Installation and Setup
The installation and setup process for this interpreter are straightforward. Follow the steps below to ensure a proper setup:

<br>

- Step 1: Fork this repository and store it in a local environment.
    
    - Start by navigating to the repository on GitHub.

    - Click on the "Fork" button in the upper-right corner to create a copy of the repository under your GitHub account.
    
    - Clone the forked repository to your local environment using Git or download it as a ZIP file and extract it.

<br>

- Step 2: Install required modules.

    - Before proceeding, ensure you have Python installed on your system.
    - Navigate to the root directory of the cloned or extracted repository in your terminal or command prompt.
    - Run the following command in your terminal to install the required modules:
    
        > pip install -r requirements.txt

<br>
<br>
<br>

# 3. Getting started

This section serves as a comprehensive guide to understanding the formatting structure of YAML scripts and how to interpret them using the provided code to create an executable Python script.

<br>

## 3.1. Formatting your YAML script

This section begins by discussing the essential task of specifying the type of operation within your YAML script. As outlined in [Section 1](#1-introduction), there are five possible operations, each identified by the key type within your YAML script.

We'll now outline the format for each type of operation and provide clear instructions on how to properly structure them.

<br>

### 3.1.1. Types of Operations: Integrations

```yaml
- type:                 integration                 [required]
alias:                  <String>                    [required]
recordID:               <String>                    [required]
params:
    - filter(s)         <String>                    [optional]
    - filter(s)         <String>                    [optional]
    - filter(s)         <String>                    [optional]
```

- `type` is a **required** parameter that defines the type of operation being performed.
- `alias` is a **required** parameter serving as the variable name storing the returned integration.
- `recordID` is a **required** parameter used to pass the record ID of the integration to retrieve.
- `params` is an **optional** parameter allowing specification of filters to apply on the fetched integration. Multiple filters may be specified as shown above.

<br>

### 3.1.2. Types of Operations: Modules